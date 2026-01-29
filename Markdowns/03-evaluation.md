# Evaluation methods

- **evaluation** (of results of a classification)
    - give a numerical mean to assess the success of the prediction
    - not unique, depends on the problem
    - examples:
        - percentage of correctly classified images is a good measure of classification accuracy for balanced datasets
        - if 0.1% of data are in class B, the prediction that all data in class A is 99.9% accurate!
    - approaches:
        - baseline model
        - confusion matrix
        - 2-class performance metrics
        - ROC curve, AUC

- **baseline model**
    - use the simplest approach for prediction
        - predict always class A
        - predict randomly (accuracy is $1/N$)
        - in time series predict the previous element
        - use simple heuristics
    - human experts' result

- **confusion matrix**
    - performance metric
    - plot predicted class vs. actual class results
    - in probability: $C_{ij} = P(\text{predicted}_i, \text{actual}_i)$ or $C_{ij} = P(\text{predicted}_i | \text{actual}_i)$

- **2-class performance metrics**
    - in case of 2 classes (positive/negative) the confusion matrix is

        | all measured| actual P | actual N |
        |-------------|----------|----------|
        | predicted P | true P   | false P  |
        | predicted N | false N  |  true N  |

    - constraints: $$\begin{align*}&\text{true P, N} + \text{false P, N} = \text{prediced P, N}\\
    &\text{true, false P} + \text{false, true N} = \text{actual P, N}\\
    &\text{actual, predicted P} + \text{actual, predicted N} =\text{all measured} \end{align*}$$
    - measures
        - accuracy: $P(\text{correct class}) = \dfrac{\text{true P}+\text{true N}}{\text{all measured}}$
        - precision: $P(\text{true P}\mid \text{predicted P}) = \dfrac{\text{true P}}{\text{predicted P}}$
        - recall (true alarm probability): $P(\text{true P} \mid \text{actual P}) = \dfrac{\text{true P}}{\text{actual P}}$
        - type-I error (false alarm probability): $P(\text{false P} \mid \text{actual N}) = \dfrac{\text{false P}}{\text{actual N}}$
        - type-II error (unobserved signal): $P(\text{false N} \mid \text{actual P}) = \dfrac{\text{false N}}{\text{actual P}}$
    - example: balanced datasets, example confusion matrix

        |1.0  | 0.5   | 0.5 |
        |-----|-------|-----|
        | 0.5 | 0.49  | 0.01|
        | 0.5 | 0.01  | 0.49|

        | accuracy | precision | recall | type-I | type-II |
        |----------|-----------|--------|--------|---------|
        |   0.98   |   0.98    |  0.98  |  0.02  |   0.02  |

    - example: inbalanced classes, classify everything to class A; confusion matrix. Problem can be seen only on type-I error!

        |1.0  | 0.99  | 0.01|
        |-----|-------|-----|
        | 1.0 | 0.99  | 0.01|
        | 0.0 | 0.0   | 0.0 |

        | accuracy | precision | recall | type-I | type-II |
        |----------|-----------|--------|--------|---------|
        |   0.99   |   0.99    |  1.0   |  1.0   |   0.0  |

- **ROC curve**,  **AUC**
    - ROC = receiver operating characteristics
    - AUC = Area under curve
    - the decicion often depends on a parameter, e.g. signal threshold
    - plot (x,y) where x=recall (true alarm rate) and y=type-I (false alarm rate)
        - very low threshold: all signals are classified positive: false positive=1.0 , recall=1.0
        - very restrictive threshold: all signals are classified negative: false positive=0.0, recall=0.0
        - ROC curve connects (0,0) to (1,1)
    - for random choice x=y: ROC curve is diagonal, AUC=0.5
    - in a sensible method an alarm true positive rate > false negative rate, ROC is above diagonal, AUC>0.5
    - AUC >0.8 is "good", AUC>0.9 is "very good"
    - example:

    <img src="../Images/ROC-example.png" alt="Alt text" width="400">