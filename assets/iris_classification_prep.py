from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path

import pandas as pd
import requests
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler


IRIS_DATASET_URLS = [
	"https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
	"https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv",
]


def _download_iris_dataframe(timeout: int = 20) -> pd.DataFrame:
	"""Download Iris dataset from public sources and return normalized dataframe."""
	last_error: str | None = None

	for url in IRIS_DATASET_URLS:
		try:
			response = requests.get(url, timeout=timeout)
			response.raise_for_status()

			if url.endswith("iris.data"):
				# UCI file has no header and may contain empty trailing lines.
				df = pd.read_csv(
					pd.io.common.StringIO(response.text),
					names=[
						"sepal_length",
						"sepal_width",
						"petal_length",
						"petal_width",
						"species",
					],
					header=None,
				)
				df = df.dropna(how="all")
				df = df[df["species"].notna()].reset_index(drop=True)
			else:
				df = pd.read_csv(pd.io.common.StringIO(response.text))
				df = df.rename(
					columns={
						"sepal_length": "sepal_length",
						"sepal_width": "sepal_width",
						"petal_length": "petal_length",
						"petal_width": "petal_width",
						"species": "species",
					}
				)

			required_cols = [
				"sepal_length",
				"sepal_width",
				"petal_length",
				"petal_width",
				"species",
			]
			if all(col in df.columns for col in required_cols):
				return df[required_cols].copy()

			last_error = f"Format kolom tidak sesuai dari URL: {url}"
		except Exception as exc:  # noqa: BLE001
			last_error = f"Gagal unduh {url}: {exc}"

	raise RuntimeError(last_error or "Gagal mengunduh dataset Iris dari sumber publik")


def train_and_save(output_dir: Path, test_size: float, random_state: int) -> None:
	output_dir.mkdir(parents=True, exist_ok=True)

	df = _download_iris_dataframe()
	features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
	target = "species"

	x = df[features]
	y_raw = df[target]

	label_encoder = LabelEncoder()
	y = label_encoder.fit_transform(y_raw)

	x_train, x_test, y_train, y_test = train_test_split(
		x,
		y,
		test_size=test_size,
		random_state=random_state,
		stratify=y,
	)

	preprocessor = ColumnTransformer(
		transformers=[
			("num", StandardScaler(), features),
		],
		remainder="drop",
	)

	clf = Pipeline(
		steps=[
			("preprocessor", preprocessor),
			("model", LogisticRegression(max_iter=1000, random_state=random_state)),
		]
	)
	clf.fit(x_train, y_train)

	y_pred = clf.predict(x_test)
	accuracy = accuracy_score(y_test, y_pred)

	with open(output_dir / "classifier.pkl", "wb") as f:
		pickle.dump(clf, f)

	with open(output_dir / "label_encoder.pkl", "wb") as f:
		pickle.dump(label_encoder, f)

	metadata = {
		"dataset": "Iris",
		"source_urls": IRIS_DATASET_URLS,
		"model": "LogisticRegression",
		"features": features,
		"classes": label_encoder.classes_.tolist(),
		"accuracy": float(accuracy),
		"train_size": int(len(x_train)),
		"test_size": int(len(x_test)),
		"random_state": random_state,
	}
	with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
		json.dump(metadata, f, indent=2, ensure_ascii=False)

	test_result = x_test.copy()
	test_result["actual"] = label_encoder.inverse_transform(y_test)
	test_result["predicted"] = label_encoder.inverse_transform(y_pred)
	test_result.to_csv(output_dir / "test_predictions.csv", index=False)

	df.to_csv(output_dir / "full_dataset.csv", index=False)

	print("=== Training Iris Selesai ===")
	print(f"Output folder : {output_dir}")
	print(f"Akurasi test  : {accuracy:.4f}")
	print("\nClassification report:")
	print(
		classification_report(
			y_test,
			y_pred,
			target_names=label_encoder.classes_,
		)
	)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Persiapan model klasifikasi Iris dari dataset publik"
	)
	parser.add_argument(
		"--output-dir",
		type=Path,
		default=Path(__file__).resolve().parent / "model" / "iris-classification",
		help="Folder output artefak model",
	)
	parser.add_argument(
		"--test-size",
		type=float,
		default=0.25,
		help="Proporsi data uji, contoh 0.25",
	)
	parser.add_argument(
		"--random-state",
		type=int,
		default=42,
		help="Seed agar split data konsisten",
	)
	args = parser.parse_args()

	train_and_save(
		output_dir=args.output_dir,
		test_size=args.test_size,
		random_state=args.random_state,
	)


if __name__ == "__main__":
	main()
