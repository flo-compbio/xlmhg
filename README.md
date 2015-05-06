# XL-mHG

The XL-mHG is a nonparametric enrichment test for ranked binary data, and an extension of the mHG test. The mHG test was developed by [Dr. Zohar Yakhini](http://bioinfo.cs.technion.ac.il/people/zohar) and colleagues.

If you use the XL-mHG in your research, please cite [Eden et al. (2007)](10.1371/journal.pcbi.0030039) and [Wagner (2015)](http://dx.doi.org/10.1101/018705).

# Requirements and Installation

This algorithm requires the Python packages NumPy and Cython, and was developed under Linux using Python 2.7. Running `make` should generate `xlmHG_cython.so`, which can then be imported from any Python script using `import xlmHG_cython`.
