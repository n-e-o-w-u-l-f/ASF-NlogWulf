#!/usr/bin/env python3
"""Publish only this reviewed, fixed alpha package; never overwrite a release."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPOSITORY = "n-e-o-w-u-l-f/ASF-NlogWulf"
TAG = "v0.1a"
ZIP_NAME = "NLogWulf-v0.1a.zip"
EXPECTED_SHA512 = "4e23690647bdfa2ef3d81346eb532e1ac7db1ff87340c992c0f0fdd02d0a5ff466af2d508393598b2d114288c41f64e77e02f367efd591bf2f545a2ef431d223"
ASSET_NAMES = (ZIP_NAME, "SHA512SUMS")
MAX_BYTES = 2 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_package(root):
    require(re.fullmatch(r"[a-f0-9]{128}", EXPECTED_SHA512),
            "Der freigeprüfte Paketwert ist noch nicht eingesetzt.")
    folder = root / "artifacts" / TAG
    assets = {name: (folder / name).read_bytes() for name in ASSET_NAMES}
    require(all(0 < len(data) <= MAX_BYTES for data in assets.values()),
            "Unerwartete Assetgröße.")
    require(hashlib.sha512(assets[ZIP_NAME]).hexdigest() == EXPECTED_SHA512,
            "ZIP stimmt nicht mit dem freigeprüften Hash überein.")
    require(assets["SHA512SUMS"].decode().strip().split() ==
            [EXPECTED_SHA512, ZIP_NAME], "Unerwartete Prüfsummendatei.")
    with zipfile.ZipFile(io.BytesIO(assets[ZIP_NAME])) as archive:
        require(sorted(archive.namelist()) == ["NLogWulf.deps.json", "NLogWulf.dll"],
                "ZIP enthält andere oder doppelte Einträge.")
        require(all(0 < item.file_size <= MAX_BYTES for item in archive.infolist()),
                "Unerwartete entpackte Dateigröße.")
        require(archive.testzip() is None, "ZIP-CRC-Prüfung fehlgeschlagen.")
    notes = (root / "Release-Notes.md").read_text(encoding="utf-8")
    require(notes.strip(), "Release-Notes fehlen.")
    return assets, notes


class AssetRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        target = urllib.parse.urlsplit(new_url)
        require(request.get_method() == "GET" and target.scheme == "https" and
                target.hostname and target.hostname.endswith(".githubusercontent.com"),
                "Unerwartete HTTP-Weiterleitung.")
        # Signed asset redirects must never receive the repository token.
        return urllib.request.Request(new_url, headers={"User-Agent": "ASF-NLogWulf-release"})


class GitHub:
    def __init__(self, token):
        self.token = token
        self.opener = urllib.request.build_opener(AssetRedirects())

    def request(self, path, method="GET", data=None, raw=False, missing=False, upload=False):
        base = "https://uploads.github.com" if upload else "https://api.github.com"
        headers = {"Authorization": "Bearer " + self.token,
                   "User-Agent": "ASF-NLogWulf-release",
                   "X-GitHub-Api-Version": "2022-11-28",
                   "Accept": "application/octet-stream" if raw else "application/vnd.github+json"}
        if isinstance(data, dict):
            data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
        elif data is not None:
            headers["Content-Type"] = "application/octet-stream"
        request = urllib.request.Request(base + path, method=method, data=data, headers=headers)
        try:
            with self.opener.open(request, timeout=30) as response:
                payload = response.read(MAX_BYTES + 1)
        except urllib.error.HTTPError as error:
            if missing and error.code == 404:
                return None
            raise RuntimeError(f"GitHub {method} {path}: HTTP {error.code}") from None
        require(len(payload) <= MAX_BYTES, "Unerwartet große GitHub-Antwort.")
        return payload if raw else json.loads(payload)


def publish(root, assets, notes):
    require(os.environ.get("GITHUB_REPOSITORY") == REPOSITORY, "Falsches Repository.")
    require(os.environ.get("GITHUB_REF") == "refs/heads/main", "Falscher Branch.")
    commit = os.environ.get("GITHUB_SHA", "")
    require(re.fullmatch(r"[a-f0-9]{40}", commit), "Ungültiger öffentlicher Commit.")
    token = os.environ.get("GH_TOKEN", "")
    require(token, "Repository-Token fehlt.")
    github = GitHub(token)
    repo = "/repos/" + REPOSITORY
    current = github.request(repo + "/git/ref/heads/main")
    require(current["object"]["sha"] == commit, "main wurde inzwischen geändert.")
    require(github.request(repo + "/git/ref/tags/" + TAG, missing=True) is None,
            "Tag existiert bereits; zuerst manuell abgleichen.")
    require(github.request(repo + "/releases/tags/" + TAG, missing=True) is None,
            "Release existiert bereits; keine Überschreibung.")
    releases = github.request(repo + "/releases?per_page=100")
    require(len(releases) < 100 and not any(item["tag_name"] == TAG for item in releases),
            "Vorhandene Releases/Drafts erfordern manuellen Abgleich.")
    print("START: öffentlicher Tag, Draft und zwei geprüfte Assets", flush=True)
    github.request(repo + "/git/refs", "POST", {"ref": "refs/tags/" + TAG, "sha": commit})
    release = github.request(repo + "/releases", "POST", {
        "tag_name": TAG, "target_commitish": commit, "name": "ASF-NLogWulf " + TAG,
        "body": notes, "draft": True, "prerelease": True})
    release_id = release["id"]
    require(isinstance(release_id, int), "Ungültige Release-ID.")
    for name, data in assets.items():
        github.request(repo + f"/releases/{release_id}/assets?name=" + urllib.parse.quote(name),
                       "POST", data, upload=True)
    draft = github.request(repo + f"/releases/{release_id}")
    require(draft["draft"] and draft["prerelease"] and draft["tag_name"] == TAG,
            "Unerwarteter Draftzustand.")
    require(sorted(asset["name"] for asset in draft["assets"]) == sorted(ASSET_NAMES),
            "Unerwartete Assetliste.")
    for asset in draft["assets"]:
        expected = assets[asset["name"]]
        require(asset["state"] == "uploaded" and asset["size"] == len(expected),
                "Asset nicht vollständig hochgeladen.")
        downloaded = github.request(repo + f"/releases/assets/{asset['id']}", raw=True)
        require(downloaded == expected, "Download stimmt nicht bytegenau überein.")
    ref = github.request(repo + "/git/ref/tags/" + TAG)
    require(ref["object"]["type"] == "commit" and ref["object"]["sha"] == commit,
            "Tag zeigt nicht auf den geprüften öffentlichen Commit.")
    github.request(repo + f"/releases/{release_id}", "PATCH",
                   {"draft": False, "prerelease": True})
    final = github.request(repo + f"/releases/{release_id}")
    require(not final["draft"] and final["prerelease"] and final["tag_name"] == TAG,
            "Öffentlicher Releasezustand nicht bestätigt.")
    print("VERIFIED: " + final["html_url"], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    assets, notes = verify_package(root)
    if args.check_only:
        print("PASS: Paket, Prüfsumme, ZIP-Allowlist und Release-Notes")
    else:
        publish(root, assets, notes)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("FEHLER: " + str(error), file=sys.stderr)
        print("Keine automatische Wiederholung: Tag/Draft/Assets vor Fortsetzung abgleichen.",
              file=sys.stderr)
        sys.exit(1)
