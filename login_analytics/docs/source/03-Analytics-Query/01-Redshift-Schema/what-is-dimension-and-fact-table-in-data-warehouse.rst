What is Dimension and Fact Table in Data Warehouse
==============================================================================


.. _dimension-table:

Dimension Table
------------------------------------------------------------------------------

- A dimension table contains dimensions of a fact.
- They are joined to fact table via a foreign key.
- Dimension tables are de-normalized tables.
- The Dimension Attributes are the various columns in a dimension table
- Dimensions offers descriptive characteristics of the facts with the help of their attributes
- No set limit set for given for number of dimensions
- The dimension can also contain one or more hierarchical relationships


.. _fact-table:

Fact Table
------------------------------------------------------------------------------

A fact table is a primary table in a `dimensional model <https://data-warehouses.net/glossary/dimensionalmodel.html>`_.

A Fact Table contains:

- Measurements/facts
- Foreign key to dimension table


Reference
------------------------------------------------------------------------------

- Difference Between Fact Table and Dimension Table: https://www.guru99.com/fact-table-vs-dimension-table.html
