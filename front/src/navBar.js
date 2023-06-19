import React from "react";
import { BrowserRouter, Route, Link } from "react-router-dom";

function NavBar() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/record">Record</Link>
        </li>
      </ul>
    </nav>
  );
}

export default NavBar;