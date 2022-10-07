package ai.h2o.targetencoding.pipeline;

import ai.h2o.targetencoding.interaction.InteractionSupport;
import hex.pipeline.FeatureTransformer;
import hex.pipeline.PipelineContext;
import water.fvec.Frame;

public class FeatureInteractionTransformer extends FeatureTransformer<FeatureInteractionTransformer> {

  private final String[] _columns;
  private final String _interaction_column;
  
  private String[] _interaction_domain;


  public FeatureInteractionTransformer(String[] columns) {
    this(columns, null);
  }
  
  public FeatureInteractionTransformer(String[] columns, String interactionColumn) {
    _columns = columns;
    _interaction_column = interactionColumn;
  }

  @Override
  protected void doPrepare(PipelineContext context) {
    assert context != null;
    assert context._params != null;
    Frame train = new Frame(context.getTrain());
    // FIXME: InteractionSupport should be improved to not systematically modify frames in-place
    int interactionCol = InteractionSupport.addFeatureInteraction(train, _columns);
    _interaction_domain = train.vec(interactionCol).domain();
    train.remove(interactionCol);
  }

  @Override
  protected Frame doTransform(Frame fr, FrameType type, PipelineContext context) {
    InteractionSupport.addFeatureInteraction(fr, _columns, _interaction_domain);  //FIXME: same as above. Also should  be able to specify the interaction column name.
    return fr;
  }
}