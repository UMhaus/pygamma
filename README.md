Distance to agreement calculations for radiotherapy dose distributions
======================================================================

RESEARCH USE ONLY

Currently an n-dimensional version of gamma evaluation is the only algorithm implemented. The resolution in the sample and reference can be difference, however each axis of sample and reference respectively must be the sample resolution.

    from dta import gamma_evaluation
    
    distance = 3                        # 3 mm
    threshold = reference.max()*0.03    # 3 % of max in reference
    sample_res, reference_res = (2, 1)  # 2 mm voxels in sample, 1 mm in ref

    gamma_map = gamma_evaluation(sample, reference,
                                 distance, threshold,
                                 (sample_res, reference_res))

## Signed Gamma Evaluation
Signed gamma evaluation makes hot and cold spots obvious in the calculated gamma map, see here for details:

    @article{mohammadi2012modification,
      title={Modification of the gamma function for the recognition of over-and under-dose regions in three dimensions},
      author={Mohammadi, Mohammad and Rostampour, Nima and Rutten, Thomas P},
      journal={Journal of medical physics/Association of Medical Physicists of India},
      volume={37},
      number={4},
      pages={200},
      year={2012},
      publisher={Medknow Publications}
    }
