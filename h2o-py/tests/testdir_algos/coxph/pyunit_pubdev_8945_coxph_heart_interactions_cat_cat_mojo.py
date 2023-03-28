import sys
import tempfile

sys.path.insert(1, "../../../")
import h2o
from tests import pyunit_utils
from h2o.estimators.coxph import H2OCoxProportionalHazardsEstimator

# this test will make sure that mojo works with enum to enum interactions for dataset with and without NAs.
def test_coxph_enum_enum_interactions_order(interaction_orders, fileName):
    data = h2o.import_file(pyunit_utils.locate(fileName))
    data['surgery'] = data['surgery'].asfactor()
    data['transplant'] = data['transplant'].asfactor()

    model = H2OCoxProportionalHazardsEstimator(start_column="start", stop_column="stop", 
                                               interaction_pairs=interaction_orders)
    model.train(x=["age", "surgery", "transplant", "C1", "C2", "C3"], y="event", 
                training_frame=data)
    pred_h2o = model.predict(data)

    # export new file (including the random columns)
    sandbox_dir = tempfile.mkdtemp()
    model.download_mojo(path=sandbox_dir)
    mojo_name = pyunit_utils.getMojoName(model._id)
    input_csv = "%s/in.csv" % sandbox_dir
    h2o.export_file(data, input_csv)
    x, pred_mojo = pyunit_utils.mojo_predict(model, sandbox_dir, mojo_name)
    pyunit_utils.compare_frames_local(pred_h2o, pred_mojo, 1, tol=1e-10)
    
def test_coxph_enum_enum_interactions():
    test_coxph_enum_enum_interactions_order([("C1", "C2"), ("C2", "C3")], "smalldata/coxph_test/heart_enum_random_cols.csv")
    test_coxph_enum_enum_interactions_order([("C2", "C3"), ("C1", "C2")], "smalldata/coxph_test/heart_enum_random_cols.csv")
    test_coxph_enum_enum_interactions_order([("C1", "C2"), ("C2", "C3")], "smalldata/coxph_test/heart_enum_random_NAs.csv")
    test_coxph_enum_enum_interactions_order([("C2", "C3"), ("C1", "C2")], "smalldata/coxph_test/heart_enum_random_NAs.csv")


if __name__ == "__main__":
    pyunit_utils.standalone_test(test_coxph_enum_enum_interactions)
else:
    test_coxph_enum_enum_interactions()
