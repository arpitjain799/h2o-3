package hex.tree.sdt;

import org.apache.commons.math3.util.Precision;
import water.Key;
import water.Keyed;

import java.util.Arrays;
import java.util.stream.Collectors;


/**
 * Compressed SDT class containing tree as array.
 */
public class CompressedSDT extends Keyed<CompressedSDT> {

    /**
     * List of nodes, for each node holds either split feature index and threshold or just decision value if it is list.
     * Shape n x 2.
     * Values of second dimension: (feature index, threshold) or (-1, decision value)
     */
    public double[][] _nodes;

    public CompressedSDT(int nodes_count) {
        _key = Key.make("CompressedSDT" + Key.rand());
        _nodes = new double[nodes_count][2];
    }

    public CompressedSDT(double[][] nodes) {
        _key = Key.make("CompressedSDT" + Key.rand());
        _nodes = nodes;
    }

    /**
     * Makes prediction by recursively evaluating the data through the tree.
     *
     * @param rowValues       - data row to find prediction for
     * @param actualNodeIndex - actual node to avaluate and then go to selected child
     * @return class label
     */
    public int predictRowStartingFromNode(final double[] rowValues, final int actualNodeIndex) {
        double featureOrDummy = _nodes[actualNodeIndex][0];
        double thresholdOrValue = _nodes[actualNodeIndex][1];
        // first value is dummy -1 means that the node is list, return value of list
        if (featureOrDummy == -1) {
            return (int) thresholdOrValue;
        }
        if (rowValues[(int) featureOrDummy] <= thresholdOrValue
                || Precision.equals(rowValues[(int) featureOrDummy], thresholdOrValue, Precision.EPSILON)) {
            return predictRowStartingFromNode(rowValues, 2 * actualNodeIndex + 1);
        } else {
            return predictRowStartingFromNode(rowValues, 2 * actualNodeIndex + 2);
        }
    }

    @Override
    public String toString() {
        return Arrays.stream(_nodes).map(n -> "(" + n[0] + "," + n[1] + ")").collect(Collectors.joining(";"));
    }

}
