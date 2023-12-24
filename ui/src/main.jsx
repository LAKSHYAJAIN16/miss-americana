import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Cookies from 'js-cookie'

import "./styles.css";
import Home from "./pages/Home";
import Onboard from "./pages/Onboard";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path : "/home",
    element : <App />
  },
  {
    path : "/onboard",
    element : <Onboard />
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router}>
      <App />
    </RouterProvider>
  </React.StrictMode>
);
