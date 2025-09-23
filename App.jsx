import React, { useState } from "react";
import jsPDF from "jspdf";
import fondUM6P from "./assets/fond_um6p.png";
import logoScales from "./assets/logo_scales.png";
import logoUM6P from "./assets/logo_um6p.png";
import robotIA from "./assets/robot_ia.png";

function App() {
const API_URL =
  (typeof import !== "undefined" && typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL)
  || (typeof process !== "undefined" && process.env?.REACT_APP_API_URL)
  || "";

  const [question, setQuestion] = useState("");
  const [reponse, setReponse] = useState("Bonjour 👋 ! Pose-moi une question.");
  const [quiz, setQuiz] = useState([]);
  const [quizUser, setQuizUser] = useState([]);
  const [quizResult, setQuizResult] = useState(null);
  const [chargement, setChargement] = useState(false);
  const [robotAnim, setRobotAnim] = useState(false);

  // Animation robot
  const animateRobot = () => {
    setRobotAnim(true);
    setTimeout(() => setRobotAnim(false), 600);
  };

  // Synthèse vocale
  const speak = (text) => {
    if ("speechSynthesis" in window) {
      const synth = window.speechSynthesis;
      synth.cancel();
      const utter = new window.SpeechSynthesisUtterance(text);
      utter.lang = "fr-FR";
      utter.rate = 1;
      synth.speak(utter);
    }
  };

  // Pose une question au backend
  const poserQuestion = async () => {
    setChargement(true);
    setQuiz([]);
    setQuizUser([]);
    setQuizResult(null);
    animateRobot();
    try {
      const res = await fetch(`${API_URL}/repondre`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setReponse(data.reponse);
    } catch (err) {
      setReponse("Erreur de connexion au serveur Professeur IA. Vérifie que le backend Python est bien lancé.");
    }
    setChargement(false);
  };

  // Reformulation intelligente (déclenchée par le bouton "Reformuler")
  const reformuler = async () => {
    setChargement(true);
    animateRobot();
    try {
      const res = await fetch(`${API_URL}/repondre`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question + " Reformule ou explique autrement.", previous: reponse })
      });
      const data = await res.json();
      setReponse(data.reponse);
    } catch (err) {
      setReponse("Erreur de connexion au serveur Professeur IA pour la reformulation.");
    }
    setChargement(false);
  };

  // Génère quiz dynamique depuis le backend
  const lancerQuiz = async () => {
    setQuiz([]);
    setQuizUser([]);
    setQuizResult(null);
    animateRobot();
    try {
      const res = await fetch(`${API_URL}/quiz`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      const quizGen = (data && data.quiz && data.quiz.length > 0) ? data.quiz : [];
      setQuiz(quizGen);
      setQuizUser(Array(quizGen.length).fill(null));
      setQuizResult(null);
    } catch (err) {
      setQuiz([]);
      setQuizUser([]);
      setQuizResult(null);
      setReponse("Impossible de générer un quiz : le backend n'est pas accessible.");
    }
  };

  const handleSelect = (idx, rep) => {
    const copy = [...quizUser];
    copy[idx] = rep;
    setQuizUser(copy);
  };

  const validerQuiz = () => {
    let score = 0;
    quiz.forEach((q, i) => {
      if (quizUser[i] === q.correct) score += 1;
    });
    setQuizResult({ score, total: quiz.length });
  };

  // Export PDF (police petite)
  const exportPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(11); // Police plus petite
    doc.text("Quiz Professeur IA SCALES", 10, 15);
    let y = 30;
    quiz.forEach((q, i) => {
      doc.setFont("helvetica", "bold");
      doc.text(`Q${i+1}. ${q.q}`, 10, y);
      y += 7;
      doc.setFont("helvetica", "normal");
      q.a.forEach((rep, idx) => {
        const selected = (quizUser[i] === idx) ? " [X]" : "";
        doc.text(`  (${String.fromCharCode(65+idx)}) ${rep}${selected}`, 12, y);
        y += 6;
      });
      doc.text(`Bonne réponse : (${String.fromCharCode(65+q.correct)}) ${q.a[q.correct]}`, 12, y);
      y += 8;
    });
    doc.setFont("helvetica", "bold");
    doc.text(`Score obtenu : ${quizResult?.score}/${quizResult?.total}`, 10, y+2);
    doc.save("quiz_resultat.pdf");
  };

  return (
    <div
      style={{
        backgroundImage: `url(${fondUM6P})`,
        backgroundSize: "cover",
        minHeight: "100vh",
        fontFamily: "Segoe UI, Arial, sans-serif"
      }}
    >
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          background: "rgba(18,22,40,0.98)",
          padding: "14px 38px 12px 38px"
        }}
      >
        <img src={logoUM6P} alt="UM6P" style={{ height: 42 }} />
        <img src={logoScales} alt="SCALES" style={{ height: 38 }} />
      </header>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          minHeight: "75vh",
          justifyContent: "center"
        }}
      >
        <div
          style={{
            background: "rgba(25,25,40,0.97)",
            color: "#fff",
            borderRadius: 38,
            padding: "32px 38px 30px 38px",
            maxWidth: 980,
            minWidth: 520,
            margin: "38px 0 16px 0",
            boxShadow: "0 8px 60px #0004",
            position: "relative"
          }}
        >
          <div style={{display:"flex", alignItems:"flex-start", gap:24, marginBottom:18}}>
            <img
              src={robotIA}
              alt="Professeur IA"
              style={{
                height:74,
                width:74,
                borderRadius:"50%",
                boxShadow:"0 2px 14px #333",
                objectFit:"cover",
                background: "#111",
                transition: "transform 0.4s, box-shadow 0.3s",
                transform: robotAnim ? "rotate(14deg) scale(1.09)" : "none",
                boxShadow: robotAnim ? "0 0 30px 7px #ff8800,0 2px 14px #333" : "0 2px 14px #333"
              }}
            />
            <div>
              <h1 style={{
                color: "#fff",
                textAlign: "left",
                margin: 0,
                fontSize: 38,
                fontWeight: 700,
                letterSpacing: 0.5
              }}>
                Bienvenue sur Professeur IA – <span style={{color:"#ff8800"}}>SCALES</span>
              </h1>
              <div style={{
                background:"rgba(255,255,255,0.13)",
                borderRadius:16, padding:"15px 26px",
                marginTop:10, fontSize:19, fontWeight:500,
                boxShadow:"0 2px 10px #2222"
              }}>
                <span style={{ color: "#fff", fontWeight:600 }}>
                  <b>Professeur IA :</b> {reponse}
                </span>
              </div>
            </div>
          </div>
          <form
            style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}
            onSubmit={e => { e.preventDefault(); poserQuestion(); }}
          >
            <input
              style={{
                width: '100%',
                padding: 12,
                borderRadius: 9,
                border: "none",
                fontSize: 18,
                background:"#fff",
                color: "#222",
                fontWeight:500
              }}
              value={question}
              onChange={e => setQuestion(e.target.value)}
              placeholder="Posez votre question ici..."
              disabled={chargement}
            />
            <button
              type="submit"
              style={{ background: "#ff8800", color: "white", borderRadius: 8, padding: "10px 22px", border: "none", fontWeight:"bold", fontSize:17 }}
              disabled={chargement || question.trim() === ""}
            >
              Envoyer
            </button>
            <button
              type="button"
              style={{ background: "#3a98ff", color: "#fff", borderRadius: 8, padding: "10px 14px", border: "none", fontWeight:"bold", fontSize:17 }}
              onClick={() => speak(reponse)}
              disabled={!reponse}
            >
              <span role="img" aria-label="Ecouter">🔊</span>
            </button>
            <button
              type="button"
              style={{ background: "#ff8800", color: "#fff", borderRadius: 8, padding: "10px 14px", border: "none", fontWeight:"bold", fontSize:17 }}
              onClick={reformuler}
            >
              Reformuler
            </button>
          </form>
        </div>
        {/* Quiz généré */}
        <div
          style={{
            background: "rgba(40,40,50,0.93)",
            borderRadius: 24,
            marginTop: 18,
            padding: "20px 28px",
            width: "88%",
            maxWidth: 820,
            boxShadow: "0 4px 28px #0002",
            color: "#fff"
          }}
        >
          <h2 style={{ color: "#fff", fontWeight:700, fontSize:22, marginBottom:10 }}>Quiz Généré :</h2>
          <div style={{ display: "flex", gap: 14, marginBottom: 12 }}>
            <button
              style={{ background: "#ff8800", color: "#fff", borderRadius: 8, padding: "10px 24px", border: "none", fontWeight:"bold", fontSize:17 }}
              onClick={lancerQuiz}
              disabled={chargement || !question}
            >
              Générer Quiz
            </button>
            {quizResult && (
              <button
                style={{ background: "#ff8800", color: "#fff", borderRadius: 8, padding: "10px 24px", border: "none", fontWeight:"bold", fontSize:17 }}
                onClick={exportPDF}
              >
                Exporter PDF
              </button>
            )}
          </div>
          {quiz.length > 0 && (
            <div style={{ marginTop: 7 }}>
              {quiz.map((q, idx) => (
                <div key={idx} style={{ marginBottom: 13 }}>
                  <b style={{fontSize:17, color:"#fff"}}>{`Q${idx + 1}. ${q.q}`}</b>
                  <div>
                    {q.a.map((rep, repIdx) => (
                      <label key={repIdx} style={{
                        display: "block",
                        marginLeft: 18,
                        fontSize: 16,
                        color: "#fff",
                        background: quizUser[idx] === repIdx ? "#ff8800" : "transparent",
                        padding: "2px 6px",
                        borderRadius: 6,
                        cursor: "pointer"
                      }}>
                        <input
                          type="radio"
                          checked={quizUser[idx] === repIdx}
                          onChange={() => handleSelect(idx, repIdx)}
                          name={`quiz_q${idx}`}
                          style={{ marginRight: 7 }}
                        /> {`${String.fromCharCode(65 + repIdx)}) ${rep}`}
                      </label>
                    ))}
                  </div>
                </div>
              ))}
              {!quizResult && (
                <button style={{ background: "#ff8800", color: "white", borderRadius: 8, padding: 10, border: "none", fontWeight: "bold", fontSize: 16, marginTop:8 }} onClick={validerQuiz}>
                  Valider mes réponses
                </button>
              )}
              {quizResult && (
                <div style={{ marginTop: 10, textAlign: "center", fontWeight: "bold", fontSize: 18, color:"#fff" }}>
                  Score : {quizResult.score}/{quizResult.total}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

