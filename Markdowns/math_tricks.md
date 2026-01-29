# Mathematical computational methods

- **ellipsoid**
    - generating function $\chi^2(x) = (x-x_0)^TC^{-1}(x-x_0)$
    - eigenvalue equation for the correlation matrix: $Cv_n=\lambda_n v_n$
    - equipotential surfaces: $x = x_0+ r\sum_n\alpha_n \sqrt{\lambda_n} v_n$, where $|\alpha|^2=1$
        - proof: $\chi^2 = r^2 \sum_{m,n} \alpha_n\alpha_m \sqrt{\lambda_n\lambda_m} v_n^T C^{-1}v_m = r^2$

- **general Gaussian generation**
    - $\xi$ random variable having $\mathcal N(0,1)$ normal distribution
    - $\eta = \sqrt{C}\xi+\mu$ has a distribution $\mathcal N(\mu,C)$