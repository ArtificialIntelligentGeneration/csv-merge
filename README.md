# csv-merge

> Tiny zero-dependency CLI for merging multiple CSV files by a shared
> key column. Built for the daily chore of stitching reports together
> when the source tool only emits one file per account.

```
$ csv-merge --key date --output combined.csv account_a.csv account_b.csv account_c.csv
✓ merged 3 files (412 rows) → combined.csv
```

## Install

```
pip install csv-merge
```

Or run directly from source:

```
python -m csv_merge --key date --output combined.csv *.csv
```

## Usage

```
csv-merge --key <COLUMN> --output <OUT.csv> [--how outer|inner] FILE...
```

| Flag        | Default | Description |
|-------------|---------|-------------|
| `--key`     | required | Column name present in every input file. Used as the join key. |
| `--output`  | required | Path for the merged CSV. |
| `--how`     | `outer` | `outer` keeps every row from any file; `inner` keeps rows present in all files. |
| `--sep`     | `,`     | Field separator. Set to `\t` for TSV. |
| `--encoding`| `utf-8` | File encoding. |

## Why this exists

The author needed it for stitching daily ad-platform CSV exports into
one file. `pandas.merge` is overkill for the job and adds a 30 MB
dependency. This is one Python file, no dependencies, MIT.

## License

MIT. See [LICENSE](./LICENSE).

## Author

[Julian Reiter](mailto:julian@aigen-agency.com).
