from models import isolation_forest, knn, lscp
import utils as ut
import features_engineering as fte


def get_percentage_of_fraudulent_transactions(data):
    """Compute the proportion of fraudulent transactions on data.

    Args:
        data (Pandas dataframe): a matrix dataframe

    Returns:
        Percentage of fraud into dataframe.
    """
    ut.save_log(f'{get_percentage_of_fraudulent_transactions.__module__} :: '
                f'{get_percentage_of_fraudulent_transactions.__name__}')

    if fte.target_label in data.columns:
        fte.fraudulent_percentage = \
            data.filter('FraudResult==1').count() / data.count()
    return fte.fraudulent_percentage


def identify_outliers(data):
    """Create outlier detectors, train it with dataframe and append
        on data these features.

    Args:
        data (Pandas dataframe): a matrix dataframe
    Returns:
        data: Dataframe with outliers columns and sum of them
    """
    ut.save_log(f'{identify_outliers.__module__} :: '
                f'{identify_outliers.__name__}')

    percent_fraudulent_transactions = \
        get_percentage_of_fraudulent_transactions(data)

    data = data.toPandas()

    data = outliers_with_isolation_forest(data,
                                          fte.numerical_features_list,
                                          fte.target_label,
                                          percent_fraudulent_transactions)

    data = outliers_with_knn(data,
                             fte.numerical_features_list,
                             fte.target_label,
                             percent_fraudulent_transactions)

    data = outliers_with_lscp(data,
                              fte.numerical_features_list,
                              fte.target_label,
                              percent_fraudulent_transactions)

    data['SumOfOutliers'] = \
        data['IsolationForest'] + data['LSCP'] + data['KNN']
    fte.update_list_features('categorical', ['SumOfOutliers'])

    return data


def outliers_with_isolation_forest(data,
                                   features_columns_list,
                                   label_column: None,
                                   percentage_of_outliers: None):
    """Usage of Isolation Forest model to predict outliers into the data

    Args:
        data (Pandas dataframe): a matrix dataframe
        features_columns_list: list of column names (list of features)
        label_column: target column name
        percentage_of_outliers: percentage of false itens (fraud into data)

     Returns:
        data: dataframe with Isolation Forest outlier column
    """
    ut.save_log(f'{outliers_with_isolation_forest.__module__} :: '
                f'{outliers_with_isolation_forest.__name__}')

    if label_column is not None:
        model = isolation_forest.train(data,
                                       features_columns_list,
                                       label_column,
                                       percentage_of_outliers)

        predictions = model.predict(data[features_columns_list])
    else:
        predictions = isolation_forest.predict(data[features_columns_list])

    data['IsolationForest'] = isolation_forest.normalize_vector(predictions)
    fte.update_list_features('categorical', ['IsolationForest'])

    return data


def outliers_with_lscp(data,
                       features_columns_list,
                       label_column: None,
                       percentage_of_outliers: None):
    """Usage of LSCP model to predict outliers into the data

    Args:
        data (Pandas dataframe): a matrix dataframe
        features_columns_list: list of column names (list of features)
        label_column: target column name
        percentage_of_outliers: percentage of false itens (fraud into data)

     Returns:
        data: dataframe with LSCP outlier column
    """
    ut.save_log(f'{outliers_with_lscp.__module__} :: '
                f'{outliers_with_lscp.__name__}')

    if label_column is not None:
        model = lscp.train(data,
                           features_columns_list,
                           label_column,
                           percentage_of_outliers)
        predictions = model.predict(data[features_columns_list])
    else:
        predictions = lscp.predict(data)

    data['LSCP'] = predictions
    fte.update_list_features('categorical', ['LSCP'])

    return data


def outliers_with_knn(data,
                      features_columns_list,
                      label_column: None,
                      percentage_of_outliers: None):
    """Usage of KNN model to predict outliers into the data

    Args:
        data (Pandas dataframe): a matrix dataframe
        features_columns_list: list of column names (list of features)
        label_column: target column name
        percentage_of_outliers: percentage of false itens (fraud into data)

     Returns:
        data: dataframe with KNN outlier column
    """
    ut.save_log(f'{outliers_with_knn.__module__} :: '
                f'{outliers_with_knn.__name__}')

    if label_column is not None:
        model = knn.train(data,
                          features_columns_list,
                          label_column,
                          percentage_of_outliers)
        predictions = model.predict(data[features_columns_list])
    else:
        predictions = knn.predict(data)

    data['KNN'] = predictions
    fte.update_list_features('categorical', ['KNN'])

    return data
