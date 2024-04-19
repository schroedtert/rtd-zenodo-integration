import requests
import textwrap
import pathlib
import warnings

zenodo_path = pathlib.Path('docs/source/ZENODO.rst')


search_query = "PedPy"
version = "v1.0.2"
record_id = None

try:
    response = requests.get(
        "https://zenodo.org/api/records",
        params={"q": search_query, "all_versions": True, "sort": "mostrecent"},
    )
    data = response.json()

    # Check for errors
    if "status" in data and data["status"] != 200:
        raise RuntimeError("Not found")
    else:
        # Print available records
        for record in data.get("hits", {}).get("hits", []):
            if (
                "version" in record["metadata"]
                and version == record["metadata"]["version"]
            ):
                record_id = record["id"]

    headers = {"accept": "application/x-bibtex"}
    response = requests.get(
        f"https://zenodo.org/api/records/{record_id}", headers=headers
    )
    response.encoding = "utf-8"

    if response.status_code == 200:
        zenodo_record = (".. code-block:: bibtex\n\n" +
                    textwrap.indent(response.text, " "*4))
    else:
        raise RuntimeError("Not found")
except Exception:
    zenodo_record = ("`Retrieve the Zenodo record here "
                    "<https://zenodo.org/record/!!!>`_")

with open(zenodo_path, 'w') as f:
    f.write(zenodo_record)

