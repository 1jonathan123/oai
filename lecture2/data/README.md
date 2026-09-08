The Allocation Helm CSVs are unmodified copies from abstractapplic / H-B-P's
[original repository](https://github.com/H-B-P/d-and-d-sci-sep-2022), retrieved
2026-09-07:

- [dset.csv](https://raw.githubusercontent.com/H-B-P/d-and-d-sci-sep-2022/main/dset.csv): historical records.
- [incoming_class.csv](https://raw.githubusercontent.com/H-B-P/d-and-d-sci-sep-2022/main/incoming_class.csv): the original 20 incoming students.

The source repository dedicates its contents to the public domain; its license is
preserved in `ALLOCATION_HELM_LICENSE`. The notebook retains the CSV's original
`Ofstev Rating` column spelling.

SHA-256 checksums:

```text
dset.csv            6a2cdd0ec591fbe9e188d275b2c4e6957ea295c3b25340a2388441be2c54ea98
incoming_class.csv  c93bb772f05dce0c9580c6f9b8a273b390667e5617cf745bd8f994585907722e
```

`potions.npz` contains fixed synthetic instrument readings and labels for Task 1
(generation seed 212). It has 100 training, 300 validation, and 300 final-test
rows. Keep its final-test arrays reserved for the notebook's submission function.
Task 2 uses the handwritten digits bundled with scikit-learn; it downloads no data.
