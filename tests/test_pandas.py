import os
from nose.tools import assert_in, assert_not_in, assert_equal
from sklearn.utils.testing import assert_true
import pandas as pd
import oddt.pandas as opd

test_data_dir = os.path.dirname(os.path.abspath(__file__))


def test_reading():
    """ Test reading molecule files to ChemDataFrame """
    df = opd.read_sdf(os.path.join(test_data_dir, 'data/dude/xiap/actives_docked.sdf'))

    # Check classes inheritance
    assert_true(isinstance(df, opd.ChemDataFrame))
    assert_true(isinstance(df, pd.DataFrame))
    assert_true(isinstance(df['mol'], opd.ChemSeries))
    assert_true(isinstance(df['mol'], pd.Series))
    assert_true(isinstance(df, pd.DataFrame))

    # Check dimensions
    assert_equal(len(df), 100)
    assert_equal(len(df.columns), 15)

    df = opd.read_sdf(os.path.join(test_data_dir, 'data/dude/xiap/actives_docked.sdf'),
                      smiles_column='smi_col')
    assert_in('smi_col', df.columns)

    df = opd.read_sdf(os.path.join(test_data_dir, 'data/dude/xiap/actives_docked.sdf'),
                      usecols=['name', 'uniprot_id', 'act'])
    assert_equal(len(df.columns), 5)  # 3 from use_cols + 1 'mol' + 1 'mol_name'
    assert_in('uniprot_id', df.columns)
    assert_not_in('smi_col', df.columns)

    # Chunk reading
    chunks = []
    for chunk in opd.read_sdf(os.path.join(test_data_dir, 'data/dude/xiap/actives_docked.sdf'), chunksize=10):
        assert_equal(len(chunk), 10)
        chunks.append(chunk)
    assert_equal(len(chunks), 10)
    df = pd.concat(chunks)

    # Check dimensions
    assert_equal(len(df), 100)