# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, 2017 Caleb Bell <Caleb.Andrew.Bell@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

from __future__ import division
from fluids import *
from math import *
import numpy as np
from scipy.integrate import quad
from numpy.testing import assert_allclose
import pytest


def test_geometry():
    SA1 = SA_partial_sphere(1., 0.7)
    SA2 = SA_partial_sphere(2, 1) # One spherical head's surface area:
    assert_allclose([SA1, SA2], [2.199114857512855, 6.283185307179586])

    V1 = V_partial_sphere(1., 0.7)
    assert_allclose(V1, 0.4105014400690663)

    # Two examples from [1]_, and at midway, full, and empty.
    Vs_horiz_conical1 = [V_horiz_conical(D=108., L=156., a=42., h=i)/231. for i in (36, 84, 54, 108, 0)]
    Vs_horiz_conical1s = [2041.1923581273443, 6180.540773905826, 3648.490668241736, 7296.981336483472, 0.0]
    assert_allclose(Vs_horiz_conical1, Vs_horiz_conical1s)

    # Head only custom example:
    V_head1 = V_horiz_conical(D=108., L=156., a=42., h=84., headonly=True)/231.
    V_head2 = V_horiz_conical(108., 156., 42., 84., headonly=True)/231.
    assert_allclose([V_head1, V_head2], [508.8239000645628]*2)

    # Two examples from [1]_, and at midway, full, and empty.
    Vs_horiz_ellipsoidal = [V_horiz_ellipsoidal(D=108., L=156., a=42., h=i)/231. for i in (36, 84, 54, 108, 0)]
    Vs_horiz_ellipsoidals = [2380.9565415578145, 7103.445235921378, 4203.695769930696, 8407.391539861392, 0.0]
    assert_allclose(Vs_horiz_ellipsoidal, Vs_horiz_ellipsoidals)

    #Head only custom example:
    V_head1 = V_horiz_ellipsoidal(D=108., L=156., a=42., h=84., headonly=True)/231.
    V_head2 = V_horiz_ellipsoidal(108., 156., 42., 84., headonly=True)/231.
    assert_allclose([V_head1, V_head2], [970.2761310723387]*2)

    # Two examples from [1]_, and at midway, full, and empty.
    V_calc = [V_horiz_guppy(D=108., L=156., a=42., h=i)/231. for i in (36, 84, 54, 108, 0)]
    Vs = [1931.7208029476762, 5954.110515329029, 3412.8543046053724, 7296.981336483472, 0.0]
    assert_allclose(V_calc, Vs)

    # Head only custom example:
    V_head1 = V_horiz_guppy(D=108., L=156., a=42., h=36, headonly=True)/231.
    V_head2 = V_horiz_guppy(108., 156., 42., 36, headonly=True)/231.
    assert_allclose([V_head1, V_head2], [63.266257496613804]*2)


    # Two examples from [1]_, and at midway, full, and empty.
    V_calc = [V_horiz_spherical(D=108., L=156., a=42., h=i)/231. for i in (36, 84, 54, 108, 0)]
    Vs = [2303.9615116986183, 6935.163365275476, 4094.025626387197, 8188.051252774394, 0.0]
    assert_allclose(V_calc, Vs)

    # Test when the integration function is called, on its limits:
    # The integral can be done analytically, but there's a zero to the power of negative integer error
    # the expression is 
    # -cmath.atan(cmath.sqrt((R ** 2 - x ** 2) / (-R ** 2 + r ** 2))) * x ** 3 / 3 + cmath.atan(cmath.sqrt((R ** 2 - x ** 2) / (-R ** 2 + r ** 2))) * r ** 2 * x + x * (R ** 2 - r ** 2) * cmath.sqrt(0.1e1 / (R ** 2 - r ** 2) * x ** 2 - R ** 2 / (R ** 2 - r ** 2)) / 6 + R ** 2 * cmath.log(x / (R ** 2 - r ** 2) * (0.1e1 / (R ** 2 - r ** 2)) ** (-0.1e1 / 0.2e1) + cmath.sqrt(0.1e1 / (R ** 2 - r ** 2) * x ** 2 - R ** 2 / (R ** 2 - r ** 2))) * (0.1e1 / (R ** 2 - r ** 2)) ** (-0.1e1 / 0.2e1) / 6 - 0.2e1 / 0.3e1 * r ** 2 * cmath.log(x / (R ** 2 - r ** 2) * (0.1e1 / (R ** 2 - r ** 2)) ** (-0.1e1 / 0.2e1) + cmath.sqrt(0.1e1 / (R ** 2 - r ** 2) * x ** 2 - R ** 2 / (R ** 2 - r ** 2))) * (0.1e1 / (R ** 2 - r ** 2)) ** (-0.1e1 / 0.2e1) - r ** 3 * cmath.atan((-2 + 2 / (R ** 2 - r ** 2) * r * (x - r)) * (0.1e1 / (R ** 2 - r ** 2) * (x - r) ** 2 + 2 / (R ** 2 - r ** 2) * r * (x - r) - 1) ** (-0.1e1 / 0.2e1) / 2) / 3 + r ** 3 * cmath.atan((-2 - 2 / (R ** 2 - r ** 2) * r * (x + r)) * (0.1e1 / (R ** 2 - r ** 2) * (x + r) ** 2 - 2 / (R ** 2 - r ** 2) * r * (x + r) - 1) ** (-0.1e1 / 0.2e1) / 2) / 3

    Vs = [V_horiz_spherical(D=108., L=156., a=i, h=84.)/231. for i in (108*.009999999, 108*.01000001)]
    V_calc = [5201.54341872961, 5201.543461255985]
    assert_allclose(Vs, V_calc)

    # Head only custom example:
    V_head1 =  V_horiz_spherical(D=108., L=156., a=42., h=84., headonly=True)/231.
    V_head2 =  V_horiz_spherical(108., 156., 42., 84., headonly=True)/231.
    assert_allclose([V_head1, V_head2], [886.1351957493874]*2)


    # Two examples from [1]_, and at midway, full, empty, and 1 inch; covering
    # all code cases.
    V_calc  = [V_horiz_torispherical(D=108., L=156., f=1., k=0.06, h=i)/231. for i in [36, 84, 54, 108, 0, 1]]
    Vs = [2028.626670842139, 5939.897910157917, 3534.9973314622794, 7069.994662924554, 0.0, 9.580013820942611]
    assert_allclose(V_calc, Vs)

    # Head only custom example:
    V_head1 = V_horiz_torispherical(D=108., L=156., f=1., k=0.06, h=36, headonly=True)/231.
    V_head2 = V_horiz_torispherical(108., 156., 1., 0.06, 36, headonly=True)/231.
    assert_allclose([V_head1, V_head2], [111.71919144384525]*2)

    # Two examples from [1]_, and at empty and h=D.
    Vs_calc = [V_vertical_conical(132., 33., i)/231. for i in [24, 60, 0, 132]]
    Vs = [250.67461381371024, 2251.175535772343, 0.0, 6516.560761446257]
    assert_allclose(Vs_calc, Vs)

    # Two examples from [1]_, and at empty and h=D.
    Vs_calc = [V_vertical_ellipsoidal(132., 33., i)/231. for i in [24, 60, 0, 132]]
    Vs = [783.3581681678445, 2902.831611916969, 0.0, 7168.216837590883]
    assert_allclose(Vs_calc, Vs)

    # Two examples from [1]_, and at empty and h=D.
    Vs_calc = [V_vertical_spherical(132., 33., i)/231. for i in [24, 60, 0, 132]]
    Vs = [583.6018352850442, 2658.4605833627343, 0.0, 6923.845809036648]
    assert_allclose(Vs_calc, Vs)

    # Two examples from [1]_, and at empty, 1, 22, and h=D.
    Vs_calc = [V_vertical_torispherical(132., 1.0, 0.06, i)/231. for i in [24, 60, 0, 1, 22, 132]]
    Vs = [904.0688283793511, 3036.7614412163075, 0.0, 1.7906624793188568, 785.587561468186, 7302.146666890221]
    assert_allclose(Vs_calc, Vs)

    # Three examples from [1]_, and at empty and with h=D.
    Vs_calc = [V_vertical_conical_concave(113., -33, i)/231 for i in [15., 25., 50., 0, 113]]
    Vs = [251.15825565795188, 614.6068425492208, 1693.1654406426783, 0.0, 4428.278844757774]
    assert_allclose(Vs_calc, Vs)

    # Three examples from [1]_, and at empty and with h=D.
    Vs_calc = [V_vertical_ellipsoidal_concave(113., -33, i)/231 for i in [15., 25., 50., 0, 113]]
    Vs = [44.84968851034856, 207.6374468071692, 1215.605957384487, 0.0, 3950.7193614995826]
    assert_allclose(Vs_calc, Vs)

    # Three examples from [1]_, and at empty and with h=D.
    Vs_calc = [V_vertical_spherical_concave(113., -33, i)/231 for i in [15., 25., 50., 0, 113]]
    Vs = [112.81405437348528, 341.7056403375114, 1372.9286894955042, 0.0, 4108.042093610599]
    assert_allclose(Vs_calc, Vs)

    # Three examples from [1]_, and at empty and with h=D.
    Vs_calc = [V_vertical_torispherical_concave(D=113., f=0.71, k=0.081, h=i)/231 for i in [15., 25., 50., 0, 113]]
    Vs = [103.88569287163769, 388.72142877582087, 1468.762358198084, 0.0, 4203.87576231318]
    assert_allclose(Vs_calc, Vs)

    SA1 = SA_ellipsoidal_head(2, 1)
    SA2 = SA_ellipsoidal_head(2, 0.999)
    SAs = [6.283185307179586, 6.278996936093318]
    assert_allclose([SA1, SA2], SAs)

    SA1 = SA_conical_head(2, 1)
    SAs = 4.442882938158366
    assert_allclose(SA1, SAs)

    SA1 = SA_guppy_head(2, 1)
    assert_allclose(SA1, 6.654000019110157)

    SA1 = SA_torispheroidal(D=2.54, fd=1.039370079, fk=0.062362205)
    assert_allclose(SA1, 6.00394283477063)

    SA1 = SA_tank(D=2, L=2)
    SA2 = SA_tank(D=1., L=0, sideA='ellipsoidal', sideA_a=2, sideB='ellipsoidal', sideB_a=2)
    SA3 = SA_tank(D=1., L=5, sideA='conical', sideA_a=2, sideB='conical', sideB_a=2)
    SA4 = SA_tank(D=1., L=5, sideA='spherical', sideA_a=0.5, sideB='spherical', sideB_a=0.5)
    SAs = [18.84955592153876, 28.480278854014387, 22.18452243965656, 18.84955592153876]
    assert_allclose([SA1, SA2, SA3, SA4], SAs)

    SA1, (SA2, SA3, SA4) = SA_tank(D=2.54, L=5, sideA='torispherical', sideB='torispherical', sideA_f=1.039370079, sideA_k=0.062362205, sideB_f=1.039370079, sideB_k=0.062362205, full_output=True)
    SAs = [51.90611237013163, 6.00394283477063, 6.00394283477063, 39.89822670059037]
    assert_allclose([SA1, SA2, SA3, SA4], SAs)

    SA1 = SA_tank(D=1., L=5, sideA='guppy', sideA_a=0.5, sideB='guppy', sideB_a=0.5)
    assert_allclose(SA1, 19.034963277504044)

    a1 = a_torispherical(D=96., f=0.9, k=0.2)
    a2 = a_torispherical(D=108., f=1., k=0.06)
    ais = [25.684268924767125, 18.288462280484797]
    assert_allclose([a1, a2], ais)

    # Horizontal configurations, compared with TankCalc - Ellipsoidal*2,
    # Ellipsoidal/None, spherical/conical, None/None. Final test is guppy/torispherical,
    # no checks available.

    Vs_calc = [V_from_h(h=h, D=10., L=25., horizontal=True, sideA='ellipsoidal', sideB='ellipsoidal', sideA_a=2, sideB_a=2) for h in [1, 2.5, 5, 7.5, 10]]
    Vs = [108.05249928250362, 416.5904542901302, 1086.4674593664702, 1756.34446444281, 2172.9349187329403]
    assert_allclose(Vs_calc, Vs)
    Vs_calc =[V_from_h(h=h, D=10., L=25., horizontal=True, sideA='ellipsoidal', sideA_a=2) for h in [1, 2.5, 5, 7.5, 10]]
    Vs = [105.12034613915314, 400.22799255268336, 1034.1075818066402, 1667.9871710605971, 2068.2151636132803]
    assert_allclose(Vs_calc, Vs)

    Vs_calc = [V_from_h(h=h, D=10., L=25., horizontal=True, sideA='spherical', sideB='conical', sideA_a=2, sideB_a=2) for h in [1, 2.5, 5, 7.5, 10]]
    Vs = [104.20408244287965, 400.47607362329063, 1049.291946298991, 1698.107818974691, 2098.583892597982]
    assert_allclose(Vs_calc, Vs)
    Vs_calc = [V_from_h(h=h, D=10., L=25., horizontal=True, sideB='spherical', sideA='conical', sideB_a=2, sideA_a=2) for h in [1, 2.5, 5, 7.5, 10]]
    assert_allclose(Vs_calc, Vs)

    Vs_calc = [V_from_h(h=h, D=1.5, L=5., horizontal=True) for h in [0, 0.75, 1.5]]
    Vs = [0.0, 4.417864669110647, 8.835729338221293]
    assert_allclose(Vs_calc, Vs)

    Vs_calc = [V_from_h(h=h, D=10., L=25., horizontal=True, sideA='guppy', sideB='torispherical', sideA_a=2, sideB_f=1., sideB_k=0.06) for h in [1, 2.5, 5, 7.5, 10]]
    Vs = [104.68706323659293, 399.0285611453449, 1037.3160340613756, 1683.391972469731, 2096.854290344973]
    assert_allclose(Vs_calc, Vs)
    Vs_calc = [V_from_h(h=h, D=10., L=25., horizontal=True, sideB='guppy', sideA='torispherical', sideB_a=2, sideA_f=1., sideA_k=0.06) for h in [1, 2.5, 5, 7.5, 10]]
    assert_allclose(Vs_calc, Vs)

    with pytest.raises(Exception):
        V_from_h(h=7, D=1.5, L=5)
        
    # bad head cases
    with pytest.raises(Exception):
        V_from_h(h=2.6, D=10., L=25., horizontal=True, sideA='BADHEAD', sideB='torispherical', sideA_a=2, sideB_f=1., sideB_k=0.06)
    with pytest.raises(Exception):
        V_from_h(h=2.6, D=10., L=25., horizontal=True, sideA='torispherical', sideB='BADHEAD', sideA_a=2, sideB_f=1., sideB_k=0.06)

    # Vertical configurations, compared with TankCalc - conical*2, spherical*2,
    # ellipsoidal*2. Torispherical*2 has no check. None*2 checks.

    Vs_calc = [V_from_h(h=h, D=1.5, L=5., horizontal=False, sideA='conical', sideB='conical', sideA_a=2., sideB_a=1.) for h in [0, 1, 2, 5., 7, 7.2, 8]]
    Vs = [0.0, 0.14726215563702155, 1.1780972450961726, 6.4795348480289485, 10.013826583317465, 10.301282311120932, 10.602875205865551]
    assert_allclose(Vs_calc, Vs)
    Vs_calc = [V_from_h(h=h, D=8., L=10., horizontal=False, sideA='spherical', sideB='spherical', sideA_a=3., sideB_a=4.) for h in [0, 1.5, 3, 8.5, 13., 15., 16.2, 17]]
    Vs = [0.0, 25.91813939211579, 89.5353906273091, 365.99554414321085, 592.190215201676, 684.3435997069765, 718.7251897078633, 726.2315017548405]
    assert_allclose(Vs_calc, Vs)
    Vs_calc = [V_from_h(h=h, D=8., L=10., horizontal=False, sideA='ellipsoidal', sideB='ellipsoidal', sideA_a=3., sideB_a=4.) for h in [0, 1.5, 3, 8.5, 13., 15., 16.2, 17]]
    Vs = [0.0, 31.41592653589793, 100.53096491487338, 376.99111843077515, 603.1857894892403, 695.3391739945409, 729.7207639954277, 737.2270760424049]
    assert_allclose(Vs_calc, Vs)
    Vs_calc = [V_from_h(h=h, D=8., L=10., horizontal=False, sideA='torispherical', sideB='torispherical', sideA_a=1.3547, sideB_a=1.3547, sideA_f=1.,  sideA_k=0.06, sideB_f=1., sideB_k=0.06) for h in [0, 1.3, 9.3, 10.1, 10.7094, 12]]
    Vs = [0.0, 38.723353379954276, 440.84578224136413, 481.0581682073135, 511.68995321687544, 573.323556832692]
    assert_allclose(Vs_calc, Vs)
    Vs_calc = [V_from_h(h=h, D=1.5, L=5., horizontal=False) for h in [0, 2.5, 5]]
    Vs = [0, 4.417864669110647, 8.835729338221293]
    assert_allclose(Vs_calc, Vs)

    with pytest.raises(Exception):
        V_from_h(h=7, D=1.5, L=5., horizontal=False)


def test_geometry_tank():
    V1 = TANK(D=1.2, L=4, horizontal=False).V_total
    assert_allclose(V1, 4.523893421169302)

    V2 = TANK(D=1.2, L=4, horizontal=False).V_from_h(.5)
    assert_allclose(V2, 0.5654866776461628)

    V3 = TANK(D=1.2, L=4, horizontal=False).h_from_V(.5)
    assert_allclose(V3, 0.44209706414415373)

    T1 = TANK(V=10, L_over_D=0.7, sideB='conical', sideB_a=0.5)
    T1.set_table(dx=0.001)
    things_calc = T1.A, T1.A_sideA, T1.A_sideB, T1.A_lateral
    things = (24.94775907657148, 5.118555935958284, 5.497246519930003, 14.331956620683194)
    assert_allclose(things_calc, things)

    L1 = TANK(D=10., horizontal=True, sideA='conical', sideB='conical', V=500).L
    D1 = TANK(L=4.69953105701, horizontal=True, sideA='conical', sideB='conical', V=500).D
    L2 = TANK(L_over_D=0.469953105701, horizontal=True, sideA='conical', sideB='conical', V=500).L
    assert_allclose([L1, D1, L2], [4.699531057009146, 9.999999999999407, 4.69953105700979])

    L1 = TANK(D=10., horizontal=False, sideA='conical', sideB='conical', V=500).L
    D1 = TANK(L=4.69953105701, horizontal=False, sideA='conical', sideB='conical', V=500).D
    L2 = TANK(L_over_D=0.469953105701, horizontal=False, sideA='conical', sideB='conical', V=500).L
    assert_allclose([L1, D1, L2], [4.699531057009146, 9.999999999999407, 4.69953105700979])

    # Test L_over_D setting simple cases
    L1 = TANK(D=1.2, L_over_D=3.5, horizontal=False).L
    D1 = TANK(L=1.2, L_over_D=3.5, horizontal=False).D
    assert_allclose([L1, D1], [4.2, 0.342857142857])
    # Test toripsherical a calculation
    V = TANK(L=1.2, L_over_D=3.5, sideA='torispherical', sideB='torispherical', sideA_f=1.,  sideA_k=0.06, sideB_f=1., sideB_k=0.06).V_total
    assert_allclose(V, 0.117318265914)

    with pytest.raises(Exception):
        # Test overdefinition case
        TANK(V=10, L=10, D=10)
    with pytest.raises(Exception):
        # Test sides specified with V solving
        TANK(V=10, L=10, sideA='conical', sideB_a=0.5)
    with pytest.raises(Exception):
        TANK(V=10, L=10, sideA='conical', sideA_a_ratio=None)
   
     
@pytest.mark.slow       
def test_geometry_tank_chebyshev():
    # Test auto set Chebyshev table
    T = TANK(L=1.2, L_over_D=3.5)
    assert_allclose(T.h_from_V(T.V_total, 'chebyshev'), T.h_max)
    T = TANK(L=1.2, L_over_D=3.5)
    assert_allclose(T.V_from_h(T.h_max, 'chebyshev'), T.V_total)


@pytest.mark.slow
def test_geometry_tank_fuzz_h_from_V():
    T = TANK(L=1.2, L_over_D=3.5, sideA='torispherical', sideB='torispherical', sideA_f=1., horizontal=True, sideA_k=0.06, sideB_f=1., sideB_k=0.06)
    T.set_chebyshev_approximators(deg_forward=100, deg_backwards=600)

    # test V_from_h - pretty easy to get right    
    for h in np.linspace(0, T.h_max, 30):
        # It's the top and the bottom of the tank that works poorly
        V1 = T.V_from_h(h, 'full')
        V2 = T.V_from_h(h, 'chebyshev')
        assert_allclose(V1, V2, rtol=1E-7, atol=1E-7)
        
    with pytest.raises(Exception):
        T.V_from_h(1E-5, 'NOTAMETHOD')

    # reverse - the spline is also pretty easy, with a limited number of points
    # when the required precision is low
    T.set_table(n=150)
    for V in np.linspace(0, T.V_total, 30):
        h1 = T.h_from_V(V, 'brenth')
        h2 = T.h_from_V(V, 'spline')
        assert_allclose(h1, h2, rtol=1E-5, atol=1E-6)

        h3 = T.h_from_V(V, 'chebyshev')
        # Even with a 600-degree polynomial, there will be failures if N 
        # is high enough, but the tolerance should just be lowered
        assert_allclose(h1, h3, rtol=1E-7, atol=1E-7)
    
    with pytest.raises(Exception):
        T.h_from_V(1E-5, 'NOTAMETHOD')

    
def test_basic():
    psi = sphericity(10., 2.)
    assert_allclose(psi, 0.767663317071005)

    a_r = aspect_ratio(.2, 2)
    assert_allclose(a_r, 0.1)

    f_circ = circularity(1.5, .1)
    assert_allclose(f_circ, 1884.9555921538756)

    A = A_cylinder(0.01, .1)
    assert_allclose(A, 0.0032986722862692833)

    V = V_cylinder(0.01, .1)
    assert_allclose(V, 7.853981633974484e-06)

    A = A_hollow_cylinder(0.005, 0.01, 0.1)
    assert_allclose(A, 0.004830198704894308)

    V = V_hollow_cylinder(0.005, 0.01, 0.1)
    assert_allclose(V, 5.890486225480862e-06)

    A =  A_multiple_hole_cylinder(0.01, 0.1, [(0.005, 1)])
    assert_allclose(A, 0.004830198704894308)

    V = V_multiple_hole_cylinder(0.01, 0.1, [(0.005, 1)])
    assert_allclose(V, 5.890486225480862e-06)
    
    
def test_HelicalCoil():
    for kwargs in [{'Do': 30, 'H': 20, 'pitch': 5, 'Dt':2},
                   {'Do': 30, 'N': 4, 'pitch': 5, 'Dt':2},
                   {'Do': 30, 'N': 4, 'H': 20, 'Dt':2},
                   {'Do_total': 32, 'N': 4, 'H': 20, 'Dt':2},
                   {'Do_total': 32, 'N': 4, 'H_total': 22, 'Dt':2}]:

        a = HelicalCoil(Di=1.8, **kwargs)
        assert_allclose(a.N, 4)
        assert_allclose(a.H, 20)
        assert_allclose(a.H_total, 22)
        assert_allclose(a.Do_total, 32)
        assert_allclose(a.pitch, 5)
        assert_allclose(a.tube_length, 377.5212621504738)
        assert_allclose(a.surface_area, 2372.0360474917497)
        # Other parameters
        assert_allclose(a.curvature, 0.06)
        assert_allclose(a.helix_angle, 0.053001960689651316)
        assert_allclose(a.tube_circumference, 94.24777960769379)
        assert_allclose(a.total_inlet_area, 3.141592653589793)
        assert_allclose(a.total_volume, 1186.0180237458749)
        # with Di specified
        assert_allclose(a.Di, 1.8)
        assert_allclose(a.inner_surface_area,  2134.832442742575)
        assert_allclose(a.inlet_area, 2.5446900494077327)
        assert_allclose(a.inner_volume, 960.6745992341587)
        assert_allclose(a.annulus_area, 0.5969026041820604)
        assert_allclose(a.annulus_volume, 225.3434245117162)
    
    # Fusion 360 agrees with the tube length.
    # It says the SA should be 2370.3726964956063057
    # Hopefully its own calculation is flawed

    # Test successfully creating a helix with 
    HelicalCoil(Di=1.8, Do=30, H=20, pitch=2, Dt=2)
    with pytest.raises(Exception):
        HelicalCoil(Di=1.8, Do=30, H=20, pitch=1.999, Dt=2)
    with pytest.raises(Exception):
        HelicalCoil(Di=1.8, Do=30, H=20, N=10.0001,  Dt=2)
        
    # Test Dt < Do
    HelicalCoil(Do=10, H=30, N=2, Dt=10)
    with pytest.raises(Exception):
        HelicalCoil(Do=10, H=30, N=2, Dt=10.00000001)
    with pytest.raises(Exception):
        HelicalCoil(Do_total=20-1E-9, H=30, N=3., Dt=10.000)
        
        
    
def test_PlateExchanger():
    ex = PlateExchanger(amplitude=5E-4, wavelength=3.7E-3, length=1.2, width=.3, d_port=.05, plates=51)
    
    assert ex.plate_exchanger_identifier == 'L3.7A0.5B45-45'
    assert_allclose(ex.amplitude, 0.0005)
    assert_allclose(ex.a, 0.0005)
    assert_allclose(ex.b, 0.001)
    assert_allclose(ex.wavelength, 3.7E-3)
    assert_allclose(ex.pitch, 3.7E-3)

    assert ex.chevron_angle == 45
    assert ex.chevron_angles == (45, 45)
    
    assert ex.inclination_angle == 45
    
    assert_allclose(ex.plate_corrugation_aspect_ratio, 0.5405405405405406)
    assert_allclose(ex.gamma, 0.5405405405405406)
    assert_allclose(ex.plate_enlargement_factor, 1.1611862034509677)
    
    assert_allclose(ex.D_eq, 0.002)
    assert_allclose(ex.D_hydraulic, 0.0017223766473078426)
    
    assert_allclose(ex.length_port, 1.25)
    
    assert_allclose(ex.A_plate_surface, 0.41802703324234836)
    assert_allclose(ex.A_heat_transfer, 20.483324628875071)
    assert_allclose(ex.A_channel_flow, 0.0003)
    assert ex.channels == 50
    assert ex.channels_per_fluid == 25
    
    ex = PlateExchanger(amplitude=5E-4, wavelength=3.7E-3, length=1.2, width=.3, d_port=.05, plates=51, chevron_angle=(30, 60))
    assert ex.chevron_angle == 45
    assert ex.chevron_angles == (30, 60)
    
    ex = PlateExchanger(amplitude=5E-4, wavelength=3.7E-3)
    

def plate_enlargement_factor_numerical(amplitude, wavelength):
    lambda1 = wavelength
    b = amplitude
    gamma = 4*b/lambda1
    
    def to_int(s):
        return (1 + (gamma*pi/2)**2*cos(2*pi/lambda1*s)**2)**0.5
    main = quad(to_int, 0, lambda1)[0]
    
    return main/lambda1

def test_plate_enhancement_factor():
    def plate_enlargement_factor_approx(amplitude, wavelength):
        # Approximate formula
        lambda1 = wavelength
        b = amplitude
        A = 2*pi*b/lambda1
        return 1/6.*(1 + (1 + A**2)**0.5 + 4*(1 + 0.5*A**2)**0.5)
    
    # 1.218 in VDI example
    phi = plate_enlargement_factor_approx(amplitude=0.002, wavelength=0.0126)
    assert_allclose(phi, 1.217825410973735)
    assert_allclose(phi, 1.218, rtol=1E-3)

    phi = plate_enlargement_factor_numerical(amplitude=0.002, wavelength=0.0126)
    assert_allclose(phi, 1.2149896289702244)
    
@pytest.mark.slow
def test_plate_enhancement_factor_fuzz():
    # Confirm it's correct to within 1E-7
    for x in np.linspace(1E-5, 100, 3):
        for y in np.linspace(1E-5, 100, 3):
            a = PlateExchanger.plate_enlargement_factor_analytical(x, y)
            b = plate_enlargement_factor_numerical(x, y)
            assert_allclose(a, b, rtol=1E-7)
            
            
def test_RectangularFinExchanger():
    PFE = RectangularFinExchanger(0.03, 0.001, 0.012)
    assert_allclose(PFE.fin_height, 0.03)
    assert_allclose(PFE.fin_thickness, 0.001)
    assert_allclose(PFE.fin_spacing, 0.012)
    
    # calculated values
    assert_allclose(PFE.channel_height, 0.029)
    assert_allclose(PFE.blockage_ratio, 0.8861111111111111)
    assert_allclose(PFE.fin_count, 83.33333333333333)
    assert_allclose(PFE.Dh, 0.01595)
    assert_allclose(PFE.channel_width, 0.011)
    
    # with layers, plate thickness, width, and length (fully defined)
    PFE = RectangularFinExchanger(0.03, 0.001, 0.012, length=1.2, width=2.401, plate_thickness=.005, layers=40)
    assert_allclose(PFE.A_HX_layer, 19.2)
    assert_allclose(PFE.layer_fin_count, 200)
    assert_allclose(PFE.A_HX, 768.0)
    assert_allclose(PFE.height, 1.4+.005)
    assert_allclose(PFE.volume, 4.048085999999999)
    assert_allclose(PFE.A_specific_HX, 189.71928956054794)
    
    
    
def test_RectangularOffsetStripFinExchanger():
    ROSFE = RectangularOffsetStripFinExchanger(fin_length=.05, fin_height=.01, fin_thickness=.003, fin_spacing=.05)
    assert_allclose(ROSFE.fin_length, 0.05)
    assert_allclose(ROSFE.fin_height, 0.01)
    assert_allclose(ROSFE.fin_thickness, 0.003)
    assert_allclose(ROSFE.fin_spacing, 0.05)
    assert_allclose(ROSFE.blockage_ratio, 0.348)
    assert_allclose(ROSFE.blockage_ratio_Kim, 0.34199999999999997)
    assert_allclose(ROSFE.alpha, 5)
    assert_allclose(ROSFE.delta, 0.06)
    assert_allclose(ROSFE.gamma, 0.06)
    assert_allclose(ROSFE.A_channel, 0.000329)
#    assert_allclose(ROSFE.SA_fin, 0.005574)
    assert_allclose(ROSFE.Dh, 0.011804808037316112)
    assert_allclose(ROSFE.Dh_Kays_London, 0.012185185185185186)
    assert_allclose(ROSFE.Dh_Joshi_Webb, 0.011319367879456085)
    
    # With layers, plate thickness, width (fully defined)
#    ROSFE = RectangularOffsetStripFinExchanger(fin_length=.05, fin_height=.01, fin_thickness=.003, fin_spacing=.05, length=1.2, width=2.401, plate_thickness=.005, layers=40)
#    assert_allclose(ROSFE.A_HX_layer, 0.267552)
