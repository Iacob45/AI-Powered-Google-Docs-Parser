import React, { useState, useEffect } from "react";
import PaginaAutentificare from "./componente/PaginaAutentificare";
import PaginaProcesare from "./componente/PaginaProcesare";
import PaginaProfilUtilizator from "./componente/PaginaProfilUtilizator";

function App() {
  const [utilizatorAutentificat, setUtilizatorAutentificat] = useState(null);
  const [panouUtilizator, setPanouUtilizator] = useState(false);

  useEffect(() => {
    const utilizatorSalvat = localStorage.getItem("utilizator");
    const panou = localStorage.getItem("panou_utilizator") === "true";
    if (utilizatorSalvat) {
      setUtilizatorAutentificat(utilizatorSalvat);
    }
    setPanouUtilizator(panou);
  }, []);

  const logout = () => {
    localStorage.removeItem("utilizator");
    localStorage.removeItem("panou_utilizator");
    setUtilizatorAutentificat(null);
    setPanouUtilizator(false);
  };

  return (
    <>
      {utilizatorAutentificat ? (
        !panouUtilizator ? (
          <div style={{ position: "relative", minHeight: "100vh" }}>
            <div
              style={{
                position: "absolute",
                top: "-60px",
                right: "40px",
                textAlign: "right",
              }}
            >
              <div style={{ marginBottom: "10px", fontWeight: "bold" }}>
                Bine ai venit, {utilizatorAutentificat}!
              </div>
              <div
                style={{
                  display: "flex",
                  gap: "10px",
                  justifyContent: "flex-end",
                }}
              >
                <button
                  onClick={logout}
                  style={{
                    backgroundColor: "#fff",
                    border: "1px solid #333",
                    color: "#333",
                    padding: "6px 12px",
                    borderRadius: "5px",
                    cursor: "pointer",
                    fontSize: "14px",
                  }}
                >
                  Logout
                </button>
                <button
                  onClick={() => {
                    setPanouUtilizator(true);
                    localStorage.setItem("panou_utilizator", true);
                  }}
                  style={{
                    backgroundColor: "#fff",
                    border: "1px solid #333",
                    color: "#333",
                    padding: "6px 12px",
                    borderRadius: "5px",
                    cursor: "pointer",
                    fontSize: "14px",
                  }}
                >
                  Contul meu
                </button>
              </div>
            </div>

            <div style={{ marginTop: "100px" }}>
              <PaginaProcesare numeUtilizator={utilizatorAutentificat} />
            </div>
          </div>
        ) : (
          <div style={{ position: "relative", minHeight: "100vh" }}>
            <div
              style={{
                position: "absolute",
                top: "-60px",
                right: "40px",
                textAlign: "right",
              }}
            >
              <div style={{ marginBottom: "10px", fontWeight: "bold" }}>
                Bine ai venit, {utilizatorAutentificat}!
              </div>
              <div
                style={{
                  display: "flex",
                  gap: "10px",
                  justifyContent: "flex-end",
                }}
              >
                <button
                  onClick={() => {
                    setPanouUtilizator(false);
                    localStorage.setItem("panou_utilizator", false);
                  }}
                  style={{
                    backgroundColor: "#fff",
                    border: "1px solid #333",
                    color: "#333",
                    padding: "6px 12px",
                    borderRadius: "5px",
                    cursor: "pointer",
                    fontSize: "14px",
                  }}
                >
                  Înapoi la procesare
                </button>
                <button
                  onClick={logout}
                  style={{
                    backgroundColor: "#fff",
                    border: "1px solid #333",
                    color: "#333",
                    padding: "6px 12px",
                    borderRadius: "5px",
                    cursor: "pointer",
                    fontSize: "14px",
                  }}
                >
                  Logout
                </button>
              </div>
            </div>

            <div style={{ marginTop: "100px" }}>
              <PaginaProfilUtilizator numeUtilizator={utilizatorAutentificat} />
            </div>
          </div>
        )
      ) : (
        <PaginaAutentificare
          onLogin={(nume) => {
            setUtilizatorAutentificat(nume);
          }}
        />
      )}
    </>
  );
}
export default App;
