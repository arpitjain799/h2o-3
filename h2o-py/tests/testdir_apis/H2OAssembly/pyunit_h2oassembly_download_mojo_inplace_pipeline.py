import sys, os
sys.path.insert(1,"../../")
from tests import pyunit_utils
from h2o.assembly import *
from h2o.transforms.preprocessing import *
from h2o.pipeline import H2OMojoPipeline


def h2oassembly_download_mojo_inplace_pipeline():
    values = [[11, 12.5, "13", 14], [21, 22.2, "23", 24], [31, 32.3, "33", 34]]
    frame = h2o.H2OFrame(
        python_obj=values,
        column_names=["a", "b", "c", "d"],
        column_types=["numeric", "numeric", "string", "numeric"])
    assembly = H2OAssembly(steps=[
        ("exp", H2OColOp(op=H2OFrame.exp, col="b")),
        ("abs", H2OColOp(op=H2OFrame.abs, col="b")),
        ("sqrt", H2OColOp(op=H2OFrame.sqrt, col="b")),
        ("add", H2OBinaryOp(op=H2OFrame.__add__, col="b", right=H2OCol("d"))),
    ])

    expected = assembly.fit(frame)
    assert_is_type(expected, H2OFrame)

    results_dir = os.path.join(os.getcwd(), "results")
    file_name = "pyunit_h2oassembly_download_mojo_inplace_pipeline"
    path = os.path.join(results_dir, file_name + ".mojo")

    mojo_file = assembly.download_mojo(file_name=file_name, path=path)
    assert os.path.exists(mojo_file)

    pipeline = H2OMojoPipeline(mojo_path=mojo_file)
    result = pipeline.transform(frame)
    assert_is_type(result, H2OFrame)
    print(expected)
    print(result)
    pyunit_utils.compare_frames(expected, result, expected.nrows, tol_numeric=1e-5)
    
    
if __name__ == "__main__":
    pyunit_utils.standalone_test(h2oassembly_download_mojo_inplace_pipeline)
else:
    h2oassembly_download_mojo_inplace_pipeline()
