import React, { useEffect, useState } from "react";
import styles from "./WarListPage.module.scss";
import { WarCard } from "./war-card/WarCard";
import { useLoaderData } from "react-router-dom";
import { War } from "../../../models/War";


export function WarListPage() {
  const [ containerStyle, setContainerStyle ] = useState<object>({});
  const wars = useLoaderData() as War[];

  useEffect(() => {
    if (wars.length < 3) {
      setContainerStyle({ justifyContent: "center" });
    }
  }, [ wars ]);

  return (
    <div className={ styles.container } style={ containerStyle }>
      { wars && wars.length ? (
        wars.map(war => (<WarCard key={ war.id } war={ war }/>))
      ) : (
        <div className={ styles.peaceTime }>
          <p>This is a time of peace...</p>
          <p>Because there are no meme wars yet</p>
        </div>
      ) }
    </div>
  );
}
