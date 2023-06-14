# Download and Pre-Process

## Download
Use the [img2dataset](https://github.com/rom1504/img2dataset) to download the train/test dataset. 

Example to run the tool:
```
img2dataset --url_list=$TXT_PATH$ --output_folder=$OUTPUT_DIR$ --resize_mode no --encode_format png --input_format txt   --encode_quality 9 --thread_count=64
```
It is worth noting that before downloading, due to our URL may has the default delimiter character `,` , so we need to make the following changes to the source code of img2dataset to set the delimiter to `\t`. 
```
anaconda3>envs>py>lib>pythonx.x>site-packages>img2dataset>reader.py>class Reader>func _save_to_arrow:line73

change the source code from:
                if self.input_format == "txt":
                    df = csv_pq.read_csv(file, read_options=csv_pq.ReadOptions(column_names=["url"]))
to:
                if self.input_format == "txt":
                    parse_options = csv_pq.ParseOptions(delimiter='\t')
                    df = csv_pq.read_csv(file, read_options=csv_pq.ReadOptions(column_names=["url"]),parse_options = parse_options)

```

## Pre-Propross
### 1.Generate LR images
Generate corresponding LR degraded images by `generate_bicubic.m`, the code is based on [BasicSR](https://github.com/rom1504/img2dataset). You will also need to modify the function's configurations and paths accordingly.

### 2.Crop to sub-images
When the resolution of the dataset , the IO time for the CPU to read images increases, which may cause IO congestion and reduce GPU utilization. In order to address this problem, at the same time, considering the resolution input  patch requirements of the network, we first crop the image (HR image) as $768\times 768$ with the overlap of $192$ by `extract_subimages.py`. You will also need to modify the function's configurations and paths accordingly.

### 3.Generate LMDB Format
We suggest to use LMDB, you need to create an LMDB database. Please refer to the specific instructions for [LMDB](https://github.com/XPixelGroup/BasicSR/blob/master/docs/DatasetPreparation_CN.md#LMDB%E5%85%B7%E4%BD%93%E8%AF%B4%E6%98%8E). Use the `create_lmdb.py` script in Python, and make sure to select the `'create_lmdb'` function. You will also need to modify the function's configurations and paths accordingly.


