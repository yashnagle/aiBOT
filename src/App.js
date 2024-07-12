import logo from "./logo.svg";
import "./App.css";
import robot_icon from "./robot_icon.png";

function App() {
  return (
    <div className="App">
      <div className="Header">
        <header className="title">
          <div className="icon-title">
            <img className="icon" src={robot_icon} alt="aiBot logo" />
            <h1 className="icon_title">aiBot</h1>
          </div>
          <h2 className="subtitle">Ask me anything!</h2>
        </header>
      </div>

      <div className="TextEntry">
        <textarea class="query-input" placeholder="Enter query here"></textarea>
        <textarea class="query-input" placeholder="Enter query here"></textarea>
      </div>
    </div>
  );
}

export default App;
