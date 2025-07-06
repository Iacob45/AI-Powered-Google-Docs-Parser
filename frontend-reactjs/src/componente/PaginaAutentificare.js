import React, { useState, useRef } from "react";

function PaginaAutentificare({ onLogin }) {
  const [esteInregistrare, setEsteInregistrare] = useState(false);
  const [nume, setNume] = useState("");
  const [parola, setParola] = useState("");
  const [email, setEmail] = useState("");
  const [eroare, setEroare] = useState("");

  const butonRef = useRef();
  const numeRef = useRef();
  const parolaRef = useRef();
  const emailRef = useRef();

  const handleEnter = (e, nextRef) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (nextRef === butonRef) {
        if (butonRef.current) {
          butonRef.current.click();
        }
      } else if (nextRef && nextRef.current) {
        nextRef.current.focus();
      }
    }
  };

  const salveazaUtilizator = (numeUtilizator) => {
    localStorage.setItem("utilizator", numeUtilizator);
    onLogin(numeUtilizator);
  };

  const trimiteAutentificare = async () => {
    if (!nume || !parola) {
      alert("Nu au fost introduse date pentru login");
      return;
    }
    try {
      const response = await fetch("http://25.29.81.125:5050/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nume, parola }),
      });
      const data = await response.json();
      if (response.ok) {
        salveazaUtilizator(nume);
      } else {
        alert(data.detail || "Eroare la autentificare");
      }
    } catch (e) {
      alert("Eroare la conectarea cu serverul");
    }
  };

  const trimiteInregistrare = async () => {
    if (!nume || !parola || !email) {
      alert("Nu au fost introduse date pentru inregistrare");
      return;
    }
    try {
      const response = await fetch("http://25.29.81.125:5050/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nume, parola, email }),
      });
      const data = await response.json();
      if (response.ok) {
        salveazaUtilizator(nume);
      } else {
        alert(data.detail || "Eroare la înregistrare");
      }
    } catch (e) {
      alert("Eroare la conectarea cu serverul");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "start",
        height: "100vh",
        paddingTop: "80px",
        fontFamily: "Arial",
        fontSize: "18px",
      }}
    >
      <h2 style={{ fontSize: "28px", marginBottom: "20px" }}>
        {esteInregistrare ? "Register" : "Login"}
      </h2>

      <input
        type="text"
        placeholder="Nume"
        value={nume}
        ref={numeRef}
        onChange={(e) => setNume(e.target.value)}
        onKeyDown={(e) => handleEnter(e, parolaRef)}
        style={{
          margin: "10px",
          padding: "10px",
          width: "280px",
          fontSize: "16px",
        }}
      />

      <input
        type="password"
        placeholder="Parolă"
        value={parola}
        ref={parolaRef}
        onChange={(e) => setParola(e.target.value)}
        onKeyDown={(e) =>
          handleEnter(e, esteInregistrare ? emailRef : butonRef)
        }
        style={{
          margin: "10px",
          padding: "10px",
          width: "280px",
          fontSize: "16px",
        }}
      />

      {esteInregistrare && (
        <input
          type="email"
          placeholder="Email"
          value={email}
          ref={emailRef}
          onChange={(e) => setEmail(e.target.value)}
          onKeyDown={(e) => handleEnter(e, butonRef)}
          style={{
            margin: "10px",
            padding: "10px",
            width: "280px",
            fontSize: "16px",
          }}
        />
      )}

      <button
        ref={butonRef}
        onClick={esteInregistrare ? trimiteInregistrare : trimiteAutentificare}
        style={{
          margin: "20px",
          padding: "10px 20px",
          width: "280px",
          fontSize: "16px",
          backgroundColor: "#63C5DA",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        {esteInregistrare ? "Register" : "Login"}
      </button>

      <div
        style={{
          fontSize: "14px",
          color: "#007BFF",
          cursor: "pointer",
          textDecoration: "underline",
        }}
        onClick={() => {
          setEsteInregistrare(!esteInregistrare);
        }}
      >
        {esteInregistrare ? "To Login" : "New account? Register now"}
      </div>

      {eroare && (
        <p style={{ color: "red", marginTop: "15px", fontSize: "14px" }}>
          {eroare}
        </p>
      )}
    </div>
  );
}

export default PaginaAutentificare;
