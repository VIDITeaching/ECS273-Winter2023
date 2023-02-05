from sklearn.datasets import fetch_openml
from sklearn.manifold import TSNE
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets, svm, metrics
import numpy as np
#
# raw_data, raw_labels = fetch_openml('mnist_784', version=1, return_X_y=True)
# nsamples = 5000
# data = raw_data[:nsamples]
# labels = raw_labels[:nsamples]
# labels_name = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
#
# data = data / 255.
# labels = labels.astype('int')
# images = data.values.reshape(data.shape[0], 28, 28)
#
# view = TSNE(n_components=2, random_state=123).fit_transform(data)
#
# points = pd.DataFrame(view, columns=['posX', 'posY'])
# points['cluster'] = labels.tolist()


def clustering_fashion_mnist() -> tuple[list[dict], list[int]]:
    digits = datasets.load_digits()
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.4, shuffle=False
    )
    view = TSNE(n_components=2, random_state=123).fit_transform(X_train)
    #
    points = pd.DataFrame(view, columns=['posX', 'posY'])
    points['cluster'] = y_train
    labels_name = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # How to JSON serialize pandas dataframes and numpy arrays
    return points.to_dict(orient='records'), list(labels_name)




def process_mnist(gamma_value: float = 0.001) -> tuple[list[dict], list[int]]:
    """Load MNIST dataset and do some basic processing
    Example 1: train an SVM model
    Args:
        gamma_value: the value of parameter gamma for SVM model
    Return:
        report (dict): report of the prediction result
    """

    if gamma_value <= 0.0001 or gamma_value >= 10:
        raise ValueError("The value of gamma should be between 0.0001 and 10.")

    digits = datasets.load_digits()

    # flatten the images
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))

    # Split data into 60% train and 40% test subsets
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.4, shuffle=False
    )
    # print(type(X_train), X_train.shape, type(y_train), y_train.shape)
    # print(type(X_test), X_test.shape, type(y_test), y_test.shape)

    # Create a classifier: a support vector classifier
    clf = svm.SVC(gamma=gamma_value)
    # Learn the digits on the train subset
    clf.fit(X_train, y_train)
    # Predict the value of the digit on the test subset
    predicted = clf.predict(X_test)
    # print(
    #     f"Classification report for classifier {clf}:\n"
    #     f"{metrics.classification_report(y_test, predicted)}\n"
    # )
    report = metrics.classification_report(y_test, predicted, output_dict=True)
    cell_dict = []
    recall_dict = []
    f1score_dict = []
    for item in report.items():
        posX = item[0]
        value_dict = item[1]
        if isinstance(value_dict, float):
            break
        cell_dict.append({"posX": posX, "posY": round(value_dict["precision"], 3)})
        recall_dict.append({"posX": posX, "posY": round(value_dict["recall"], 3)})
        f1score_dict.append({"posX": posX, "posY": round(value_dict["f1-score"], 3)})

    data_result = []
    data_result = np.append(data_result, dict(name='precision', values=cell_dict))
    data_result = np.append(data_result, dict(name='recall', values=recall_dict))
    data_result = np.append(data_result, dict(name='f1-score', values=f1score_dict ))

    cluster_labels = ["precision", "recall", "f1-score"]
    return data_result.tolist(), cluster_labels
