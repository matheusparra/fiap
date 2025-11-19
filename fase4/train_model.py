"""
Treinamento de modelo de predição de irrigação (Fase 4).

Este script treina um modelo simples de RandomForestClassifier utilizando
dados sintéticos de umidade e estado de irrigação.  Serve apenas como
exemplo.  Para treinar um modelo real, substitua o gerador de dados por
leituras do banco de dados e labels reais.
"""
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def gerar_dados(n_samples: int = 200) -> tuple[np.ndarray, np.ndarray]:
    """Gera dados sintéticos.
    Umidade < 30 → classe 1 (irrigar), caso contrário classe 0.
    """
    X = np.random.uniform(0, 100, size=(n_samples, 1))  # umidade
    y = (X.flatten() < 30).astype(int)
    return X, y


def treinar_modelo() -> RandomForestClassifier:
    X, y = gerar_dados()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acc:.3f}")
    return clf


def main() -> None:
    clf = treinar_modelo()
    with open("model.pkl", "wb") as f:
        pickle.dump(clf, f)
    print("Modelo salvo em model.pkl")


if __name__ == "__main__":
    main()