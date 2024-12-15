<div align="left">
  <h1>Bigbytes</h1>
</div>



Bigbytes is a hybrid framework for transforming and integrating data. It combines the best of both worlds: the flexibility of notebooks with the rigor of modular code.

- Extract and synchronize data from 3rd party sources.
- Transform data with real-time and batch pipelines using Python, SQL, and R.
- Load data into your data warehouse or data lake using our pre-built connectors.
- Run, monitor, and orchestrate thousands of pipelines without losing sleep.


## 🏃‍♀️ Install

The recommended way to install the latest version of Bigbytes is through Docker with the following command:

```bash
docker pull getbigbytes/bigbytes:latest
```

You can also install Bigbytes using pip or conda, though this may cause dependency issues without the proper environment.

```bash
pip install bigbytes
```
```bash
conda install -c conda-forge bigbytes
```

Looking for help? The _fastest_ way to get started is by checking out our documentation [here](https://docs.bigbytes.ai/getting-started/setup).

Looking for quick examples? Open a [demo](https://demo.bigbytes.ai/) project right in your browser or check out our [guides](https://docs.bigbytes.ai/guides/overview).

## 🎮 Demo

### Live demo

Build and run a data pipeline with our <b>[demo app](https://demo.bigbytes.ai/)</b>.

> WARNING
>
> The live demo is public to everyone, please don’t save anything sensitive (e.g. passwords, secrets, etc).

<sub><i>Click the image to play video</i></sub>


<b>A sample data pipeline defined across 3 files ➝</b>

1. Load data ➝
    ```python
    @data_loader
    def load_csv_from_file() -> pl.DataFrame:
        return pl.read_csv('default_repo/titanic.csv')
    ```
1. Transform data ➝
    ```python
    @transformer
    def select_columns_from_df(df: pl.DataFrame, *args) -> pl.DataFrame:
        return df[['Age', 'Fare', 'Survived']]
    ```
1. Export data ➝
    ```python
    @data_exporter
    def export_titanic_data_to_disk(df: pl.DataFrame) -> None:
        df.to_csv('default_repo/titanic_transformed.csv')
    ```

