# Data Engineering assignment
This project provides a comprehensive end-to-end solution for Medallion structure ETL using ADF and Databricks as well as fetching Data from api end point




# ADF Implementation

This project demonstrates the creation and management of various Azure resources as part of a data pipeline setup. Below are the resources created for this project:

<details>
  <summary><strong>1. ADF Pipeline Implementation</strong></summary>

  ### Creating Parent Pipeline
  ![Creating Parent Pipeline](https://github.com/shamsaravaiah/DE-assignment-implementation/blob/main/ADF%20implementation/Screenshots/parent%20pipeline.png)
  In the parent pipeline, I iteratate over the sales-view-devtst container to get the metadata at the container level, which will result in the folders [customer, product, sales store] as child items
  the will be passed into the execute pipeline activity which runs the child pipleline. 
  ### Creating Child Pipeline
  ![Creating Child Pipeline](https://github.com/shamsaravaiah/DE-assignment-implementation/blob/main/ADF%20implementation/Screenshots/child%20pipeline.png)
  The child pipeline takes the current item in the forEach actiity and passes into the pipeline level parameter that I have configured for the child Pipeline.
  The current folder is passed to the getMetadata activity insdie the forEach activity of the child pipeline which results in an array of child items as lastModified date and file name
  ### Inside forEach Activity in Child Pipeline
  ![Inside forEach Activity in Child Pipeline](https://github.com/shamsaravaiah/DE-assignment-implementation/blob/main/ADF%20implementation/Screenshots/inside%20forEach%20activity%20of%20child%20pipeline.png)
  I have assigned a pipeline level variable and assigned an old date value. Inside the forEach activity of the child pipeline I compare the data variable with the lastModified of the current file, if greater I swap the date variable with lastModified to
  preserve the latest date. I then assign the filename to a variable using Setvariable activity
  Then i copy the file to the destination using the lastet file name using the copyData activity

</details>
  
  
</details>

<details>
  <summary><strong>2. Creating a Storage Account Resource</strong></summary>
  
  ![Created Storage Account Resource](https://github.com/shamsaravaiah/Azure-Data-Pipeline/blob/main/Screen%20shots/created%20storage%20account%20resource.png)
  
</details>

<details>
  <summary><strong>3. Creating a Key Vault Resource</strong></summary>
  
  ![Created Key Vault Resource](https://github.com/shamsaravaiah/Azure-Data-Pipeline/blob/main/Screen%20shots/created%20key%20vault%20resource.png)
  
</details>

<details>
  <summary><strong>4. Creating a Databricks Workspace</strong></summary>
  
  ![Created Databricks Workspace](https://github.com/shamsaravaiah/Azure-Data-Pipeline/blob/main/Screen%20shots/created%20Databricks%20workspace.png)
  
</details>

<details>
  <summary><strong>5. Creating an Azure Data Factory Resource</strong></summary>
  
  ![Created Azure Data Factory Resource](https://github.com/shamsaravaiah/Azure-Data-Pipeline/blob/main/Screen%20shots/created%20ADF%20resource.png)
  
</details>


# Databricks Implementation


