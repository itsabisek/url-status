import logo from "./logo.svg";
import bg from "./bg.jpg"
import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { SearchOutlined, CheckRounded, CloseRounded, WarningRounded } from "@material-ui/icons";
import { IconButton } from "@material-ui/core";

export const App = () => {
  const [iconState, setIconState] = useState("none");
  const onSearch = (searchString) => {
    axios({
      method: "get",
      url: "http://127.0.0.1:5000/api/check",
      params: {
        url: searchString,
      },
    })
      .then((res) => {
        console.log(res);
        switch(res.data['error']) {
          case 1:
            setIconState("ok")
            break
          default:
            setIconState("fail")
            break
        }
          
      })
      .catch((_err) => {
        console.log(_err);
        setIconState("err");
      });
  };

  useEffect(() => {
    if (iconState === "ok" || iconState === "err" || iconState === "fail") {
      setTimeout(() => {
        setIconState("none");
      }, 3000);
    }
  });

  return (
    <div className="App">
      <div style={{backgroundImage: `url(${bg})`}} className="App-bg">
        <img src={logo} className="App-logo" alt="logo" />
        <div className="search_container">
          <input type="text" className="search_input" id="ss" />
          {iconState === "none" && (
            <IconButton
              onClick={(e) => onSearch(document.getElementById("ss")?.value)}
            >
              <SearchOutlined />
            </IconButton>
          )}
          {iconState === "ok" && (
            <IconButton disableRipple disableTouchRipple>
              <CheckRounded htmlColor="green" />
            </IconButton>
          )}
          {iconState === "fail" && (
            <IconButton disableRipple disableTouchRipple>
              <WarningRounded htmlColor="orange" />
            </IconButton>
          )}
          {iconState === "err" && (
            <IconButton disableRipple disableTouchRipple>
              <CloseRounded htmlColor="red" />
            </IconButton>
          )}
        </div>
      </div>
    </div>
  );
};
