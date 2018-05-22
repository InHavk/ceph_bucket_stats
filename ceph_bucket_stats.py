from sys import stdin
import json

html_head = """
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap4.min.js"></script>
    <script>$(document).ready(function() {
        $('#counters').DataTable({"paging": false, "order": [[ 2, "desc" ]]});
    } );</script>
  </head>
  <body>
    <table id="counters" class="table">
      <thead class="thead-dark">
        <th scope="col">Bucket name</th>
        <th scope="col">Owner</th>
        <th scope="col">Usage (kb)</th>
      </thead>
      <tbody>"""
html_table_item = """<tr><td>{}</td><td>{}</td><td>{}</td></tr>"""
html_bottom = """
      </tbody>
    </table>
  </body>
</html>"""


def parse_stream(stream):
    raw_context = stream.read()
    json_context = json.loads(raw_context)
    return json_context


def main():
    print(html_head)
    jc = parse_stream(stdin)
    for bucket in jc:
        name = bucket["bucket"]
        owner = bucket["owner"]
        usage = 0
        if bucket["usage"].get("rgw.main", None) is not None:
            usage = bucket["usage"].get("rgw.main").get("size_kb")
        print(html_table_item.format(name, owner, usage))
    print(html_bottom)


if __name__ == "__main__":
    main()
