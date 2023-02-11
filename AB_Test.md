# AB Test

## Basics

#### Population

It is the entire group that you want to draw conclusions about.

#### Sample

A sample is a small portion of a population that is representative of the characteristics of the larger population. *In A/B testing, a sample is the randomly selected set of visitors we display each of our page variations to — control is exposed to one sample and treatment is exposed to another.*

#### Sample Mean

For a given metric, this is the mean or average based on data collected for the sample. *For our A/B test example that is aiming to optimize CTR (click-through rate), this is nothing but the average CTR for users in each sample.*

#### Sample Variability

Two randomly selected samples from a population may be different from each other. Sampling variability will decrease as sample size increases. *In A/B testing, the sampling variability affects the sample size we need in order to have a chance of deriving statistically significant results.*



## Experiment Design

#### Null Hypothesis

You decide what you are trying to provide evidence for — which is the alternate hypothesis, then you set up the opposite as the null hypothesis and find evidence to disprove that. *In our A/B test example, the null hypothesis is that the population CTR on the original page and the page variation are not different.*

#### Key Metrics

A set of metrics that you are trying to optimize through the experiment. *Some commonly used metrics are click through rates (CTR), sign up rate, engagement rate, average revenue per order, retention rates*. 

#### Overall Evaluation Criteria (OEC)

When there are multiple metrics to be optimized through the experiment, it is helpful to formulate trade-offs by devising a single metric called an Overall Evaluation Criteria (OEC) — which is essentially a weighted combination of such objectives. *One way to do this is to normalize each metric to a predefined range, say 0–1, and assign each a weight. Your OEC then is the weighted some of the normalized metrics.*

#### Guardrail Metrics

These are metrics that are important for the company and should not be negatively impacted by the experiment.

#### Randomization Unit

Proper randomization is important to ensure that populations assigned to the different variants are similar statistically. Randomization unit should be chosen such that Stable unit treatment value assumptions (SUTVA) are satisfied. SUTVA states that experiment units do not interfere with one another i.e. the behavior of units in test and control is independent of each other. 

#### Interference

Sometimes also called spillover or leakage occurs when the behavior of the control group is influenced by the treatment given to the test group.

- Direct — two units can be directly connected if they are friends on a social network or if they visited the same physical space at the same time.
- Indirect — indirect connections are connections that exist because of certain shared resources. For e.g. If the Airbnb marketplace improved conversion flow for treatment users, resulting in more bookings, it would naturally lead to less inventory for Control users. Similarly marketplaces such as Lyft/Uber/Doordash where users in control and treatment might share the same pool of drivers/dashers will also face interference.



## Sample size calculation

#### Confidence Level

Confidence level refers to the percentage or probability or certainty, that the confidence interval would contain the true population parameter when you draw a random sample many times.

![img](https://miro.medium.com/max/980/1*8NVfLkzhDS-EEkjFgGTn7w.png)

#### Margin of Error

A margin of error tells you how many percentage points your results will differ from the real population value. 

#### Confidence Interval

A confidence interval gives an estimated range of values which is likely to include an unknown population parameter, the estimated range being calculated from a given set of sample data. *The width of confidence interval depends on 3 things — the **variation within the population** of interest, **the size of the sample** and the **confidence level** we are seeking.*

![img](https://miro.medium.com/max/980/1*UhVzAcRSIXdLoRbcw5D16g.png)

#### Type 1 Error $\alpha$

A type I error occurs when we incorrectly reject the null hypothesis.

#### Type 2 Error $\beta$

A type II error occurs when the null hypothesis is false, but we incorrectly fail to reject it.

#### P-value

The p-value tells you how likely it is that your data could have occurred under the null hypothesis.

#### Statistical Significance

Statistical significance is attained when the p-value is less than the significance level. The significance level ($\alpha$), is the threshold you want to use for the probability of making Type 1 error.

#### Statistical Power 

Statistical Power, which as we know is the probability that a test correctly rejects the null hypothesis i.e. the percentage of time the minimal effect will be detected, if it exists.

#### Minimum Detectable Effect (MDE)

The smallest change in conversion rate you are interested in detecting.

#### Sample Size

The number of units per variation needed to reach statistical significance, given the baseline conversion, minimum detectable difference (MDE), significance level & statistical power chosen.
$$
c = u_0 + t_{\alpha/2}\sqrt{\frac{\sigma}{n}} \\
c = u_A - t_\beta \sqrt{\frac{\sigma}{n}} \\
\Rightarrow n = \frac{(t_{\alpha/2} + t_\beta)^2\sigma^2}{(u_A - u_0)^2}
$$
If the same mean is larger than $c$, we will reject the null hypothesis $u_0$, $c$ also needs to be defined to ensure the power is $1-\beta$, which means there is a $\beta$ chance we fail to reject the null hypothesis.



## Threats to experiment validity

#### Novelty Effect

Sometimes there’s a “novelty effect” at work. Any change you make to your website will cause your existing user base to pay more attention. Changing that big call-to-action button on your site from green to orange will make returning visitors more likely to see it, if only because they had tuned it out previously. This type of effect is not likely to last in the long run — but it can artificially impact your test results.

#### Primacy effect 

When there’s a change in the product, people react to it differently. Some users may be used to the way a product works and are reluctant to change. This is called primacy effect. The primacy effect is nothing but the tendency to remember the first piece of information we encounter better than information presented later on. This can be thought of as an **opposite phenomenon to novelty effect**.

#### Seasonality

Businesses may have different user behavior say on 1st of a month and 15th of a month. For some eCommerce sites, their traffic and sales are not stable all over the year, they tend to peak on Black Friday and Cyber Mondays for example. Variability due to these factors could influence your test results.

#### Day of week effect 

Similar to seasonality, a metric may have cyclicity based on day of week. For e.g. say conversion rates are much higher on Thursdays than they are on the weekends. In this case, it is important to run tests for full-week increments, so you are including every day of the week.