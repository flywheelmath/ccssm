# ccssm
Data tools for the Common Core State Standards for Mathematics

## Dependency graph

The Common Core Mathematics standards and the logical dependencies and conceptual connections between them are represented by the dependency graph: [https://flywheelmath.github.io/ccssm/](https://flywheelmath.github.io/ccssm/)

## JSON files

The ccssm-k8.json and ccssm-hs.json contain the data of (most of) the Common Core Mathematics standards for K-8 and High School, respectively.
The file ccssm-dependencies.json lists logical dependencies and conceptual connections between the various standards.

### CSV files

For ease of use, the data from each of these JSON files is contained in the analogous CSV files.

### Python scripts

There is a script to convert between JSON and CSV formats.
There is also a script to extract the data from the JSON files into a format that can be used to generate a dependency graph.

## Acknowledgements

This project was made possible by the foundational work of others.

The initial K-8 standards data and the dependency relationships were derived from the "Common Core Mathematics Standards" project created by **Jeff Baumes**. The original data was instrumental in building this dataset.
* **Original Project Link:** [https://github.com/jeffbaumes/standards](https://github.com/jeffbaumes/standards)
* **Original Interactive Visualization:** [https://jeffbaumes.github.io/standards/](https://jeffbaumes.github.io/standards/)

The text of the Common Core State Standards is copyrighted by the National Governors Association Center for Best Practices (NGA Center) and the Council of Chief State School Officers (CCSSO) and is used here under their public license.
> © Copyright 2010. National Governors Association Center for Best Practices and Council of Chief State School Officers. All rights reserved.

## License

The code and data files in this repository are licensed under the **MIT License**.

The original data from Jeff Baumes' project, which was used as a source for this project, is licensed under the **Apache License 2.0**. A `NOTICE` file is included in this repository to comply with its attribution requirements.
