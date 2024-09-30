# Data Engineering assignment
This project provides a comprehensive end-to-end solution for Medallion structure ETL using ADF and Databricks as well as fetching Data from api end point




# ADF Implementation

The data flow process is orchestrated using ADF pipeline, with and parent and child pipelines to move latest files from each folder and coopy to correspondind destination folders in destination container:

<details>
  <summary><strong>1. ADF Pipeline Implementation (with diagrams and explanation)</strong></summary>
  
  ### Creating Parent Pipeline
  ![Creating Parent Pipeline](https://raw.githubusercontent.com/shamsaravaiah/DE-assignment-implementation/main/ADF%20implementation/Screenshots/parent%20pipeline.png)
  In the parent pipeline, I iterate over the sales-view-devtst container to get the metadata at the container level, which will result in the folders [customer, product, sales store] as child items that will be passed into the execute pipeline activity which runs the child pipeline. 
  
  ### Creating Child Pipeline
  ![Creating Child Pipeline](https://raw.githubusercontent.com/shamsaravaiah/DE-assignment-implementation/main/ADF%20implementation/Screenshots/child%20pipeline.png)
  The child pipeline takes the current item in the forEach activity and passes it into the pipeline level parameter that I have configured for the child Pipeline. The current folder is passed to the getMetadata activity inside the forEach activity of the child pipeline, resulting in an array of child items with the lastModified date and file name.
  
  ### Inside forEach Activity in Child Pipeline
  ![Inside forEach Activity in Child Pipeline](https://raw.githubusercontent.com/shamsaravaiah/DE-assignment-implementation/main/ADF%20implementation/Screenshots/inside%20forEach%20activity%20of%20child%20pipeline.png)
  I have assigned a pipeline level variable and assigned an old date value. Inside the forEach activity of the child pipeline, I compare the date variable with the lastModified of the current file. If greater, I swap the date variable with lastModified to preserve the latest date. I then assign the filename to a variable using the SetVariable activity. Then I copy the file to the destination using the latest file name with the Copy Data activity. The aim is to extract fresh and latest files from the source and copy them to the destination.

</details>

<details>
  <summary><strong>2. Resources I have used for the ADF implementation</strong></summary>
  - ADF (data flow orchestration)
  - ADLS Gen 2 (storage purpose, hierarchical namespace)
  - Databricks (to perform transformations on the source datasets prior to saving in the next layer)
</details>






# Databricks Implementation

<details>
  <summary><strong>3. Heading 3</strong></summary>
    
</details>

<details>
  <summary><strong>4. heading 4</strong></summary>
    
</details>
