import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Homepage from "./components/Homepage";
import RequestForm from "./components/RequestForm";

const App = () => {
  return (
    <Router>
      <main className="App">
        <Route exact path="/" component={Homepage} />
        <Route exact path="/request" component={RequestForm} />
      </main>
    </Router>
  );
};

export default App;
