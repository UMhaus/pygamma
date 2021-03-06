# License & Copyright
# ===================
#
# Copyright 2012 Christopher M Poole
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# 
# Distance to Agreement using Gamma Evaluation
# 
# Author:    Christopher M Poole
# Email:     mail@christopherpoole.net
# Date:      20st April, 2012


import numpy

from math import ceil
from scipy.ndimage.filters import generic_filter


def gamma_evaluation(sample, reference, distance, threshold, resolution, signed=False):
    """
    Distance to Agreement between a sample and reference using gamma evaluation.

    Parameters
    ----------
    sample : ndarray
        Sample dataset, simulation output for example
    reference : ndarray
        Reference dataset, what the `sample` dataset is expected to be
    distance : int
        Search window limit in the same units as `resolution`
    threshold : float
        The maximum passable deviation in `sample` and `reference`
    resolution : tuple
        The resolution of each axis of `sample` and `reference`
    signed : bool
        Returns signed gamma for identifying hot/cold fails

    Returns
    -------
    gamma_map : ndarray
        g == 0     (pass) the sample and reference pixels are equal
        0 < g <= 1 (pass) agreement within distance and threshold
        g > 1      (fail) no agreement 
    """
    
    ndim = len(resolution)
    assert sample.ndim == reference.ndim == ndim, \
        "`sample` and `reference` dimensions must equal `resolution` length"
    assert sample.shape == reference.shape, \
        "`sample` and `reference` must have the same shape"
    
    resolution = numpy.array(resolution)[[numpy.newaxis for i in range(ndim)]].T
    slices = [slice(-ceil(distance/r), ceil(distance/r)+1) for r in resolution]
    
    kernel = numpy.mgrid[slices] * resolution
    kernel = numpy.sum(kernel**2, axis=0) # Distance squared from central voxel.
    kernel[numpy.where(numpy.sqrt(kernel) > distance)] = numpy.inf
    kernel = kernel / distance**2
    
    footprint = numpy.ones_like(kernel)
    kernel = kernel.flatten()
    values = (reference - sample)**2 / (threshold)**2
    
    gamma_map = generic_filter(values, \
        lambda vals: numpy.minimum.reduce(vals + kernel), footprint=footprint)
    gamma_map = numpy.sqrt(gamma_map)

    if (signed):
        return gamma_map * numpy.sign(sample - reference)
    else:
        return gamma_map
    
