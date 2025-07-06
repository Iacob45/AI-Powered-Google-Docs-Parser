import React, { useEffect, useState } from "react";

function PaginaProfilUtilizator({ numeUtilizator }) {
  const [orare, setOrare] = useState([]);
  const [indexCurent, setIndexCurent] = useState(0);
  const [email, setEmail] = useState("");

  useEffect(() => {
    const fetchDate = async () => {
      try {
        const orareResp = await fetch(
          `http://25.29.81.125:5050/orare-utilizator/${numeUtilizator}`
        );
        const orareData = await orareResp.json();
        setOrare(orareData);

        const userResp = await fetch(
          `http://25.29.81.125:5050/utilizator/${numeUtilizator}`
        );
        const userData = await userResp.json();
        setEmail(userData.email);
      } catch (e) {
        alert("Eroare la încărcarea datelor utilizatorului:", e);
      }
    };

    fetchDate();
  }, [numeUtilizator]);

  const stergeOrar = async () => {
    const orarDeSters = orare[indexCurent];
    try {
      const response = await fetch("http://25.29.81.125:5050/orar/sterge", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orarDeSters),
      });
      if (!response.ok) {
        const e = await response.json();
        alert("Eroare la ștergerea orarului");
        return;
      }
      const orareNoi = [...orare];
      orareNoi.splice(indexCurent, 1);
      setOrare(orareNoi);
      setIndexCurent(Math.max(0, indexCurent - 1));
    } catch (e) {
      alert("Eroare la ștergerea orarului");
    }
  };

  const orarCurent = orare[indexCurent];

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", paddingTop: "50px" }}>
      <h2>Profil Utilizator</h2>
      <p>
        <strong>Nume utilizator:</strong> {numeUtilizator}
      </p>
      <p>
        <strong>Email:</strong> {email}
      </p>
      <p>
        <strong>Număr orare salvate:</strong> {orare.length}
      </p>

      {orarCurent && (
        <div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "10px",
            }}
          >
            <div
              style={{
                display: "flex",
                gap: "10px",
                alignItems: "center",
                marginBottom: "15px",
              }}
            >
              {indexCurent > 0 && (
                <button
                  onClick={() => setIndexCurent(indexCurent - 1)}
                  style={{
                    padding: "10px 20px",
                    fontSize: "16px",
                    color: "white",
                    backgroundColor: "#6db8d6",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                  }}
                >
                  Înapoi
                </button>
              )}
              {indexCurent < orare.length - 1 && (
                <button
                  onClick={() => setIndexCurent(indexCurent + 1)}
                  style={{
                    padding: "10px 20px",
                    fontSize: "16px",
                    color: "white",
                    backgroundColor: "#6db8d6",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                  }}
                >
                  Înainte
                </button>
              )}
            </div>
            <button
              onClick={stergeOrar}
              style={{
                padding: "10px 20px",
                fontSize: "16px",
                backgroundColor: "#fff",
                border: "2px solid red",
                color: "red",
                borderRadius: "5px",
                cursor: "pointer",
                marginLeft: "auto",
              }}
            >
              Șterge orar
            </button>
          </div>

          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead style={{ backgroundColor: "#63C5DA", color: "white" }}>
              <tr>
                <th>Nume</th>
                <th>Profesor</th>
                <th>Sala</th>
                <th>Zi</th>
                <th>Interval</th>
                <th>Durata</th>
                <th>Grupe</th>
                <th>Anul</th>
                <th>Categorie</th>
                <th>Paritate</th>
              </tr>
            </thead>
            <tbody>
              {orarCurent.activitati.map((act, index) => (
                <tr
                  key={index}
                  style={{
                    backgroundColor: index % 2 === 0 ? "#f9f9f9" : "#ffffff",
                  }}
                >
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.nume}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.profesor}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.sala}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.zi}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.interval}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.durata}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.grupe.join(", ")}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.anul}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.categorie}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {act.paritate}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default PaginaProfilUtilizator;
