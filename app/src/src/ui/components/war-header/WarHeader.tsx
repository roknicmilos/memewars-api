import React from "react";
import styles from "./WarHeader.module.scss";
import dropdownVG from "../../../assets/dropdown.svg";
import { War } from "../../../models/war";

interface InfoItem {
  label: string;
  value: string | number | boolean;
}

interface WarHeaderProps {
  war: War;
  onClick(): void;
  isOpened?: boolean;
  extraInfoItems?: InfoItem[];
}

export function WarHeader({ war, onClick, isOpened, extraInfoItems = [] }: WarHeaderProps) {
  const infoItems: InfoItem[] = [
    { label: "Phase", value: war.phase },
    { label: "Memes", value: war.meme_count },
    { label: "Requires approval of memes?", value: war.requires_meme_approval },
    ...extraInfoItems,
  ];

  const dropdownArrowClasses = [
    styles.dropdownArrow,
    isOpened ? styles.dropdownArrowRotated : "",
  ].join(" ");

  const dropdownContentStyle = {
    height: `${ isOpened ? infoItems.length * 31 + 20 : 0 }px`,
    margin: `${ isOpened ? 6 : 0 }px`,
  };

  return (
    <div className={ styles.warHeader }>
      <div className={ styles.titleDropdownButton } onClick={ onClick }>
        <h1 className={ styles.title }>{ war.name }</h1>
        <img className={ dropdownArrowClasses } src={ dropdownVG } alt="carrot"/>
      </div>
      <div className={ styles.titleDropdownContent } style={ dropdownContentStyle }>
        <div className={ styles.warInfo }>
          { infoItems.map(item => (
            <p className={ styles.infoItem }>
              <span>{ item.label }: </span>
              <span>{ item.value }</span>
            </p>
          )) }
        </div>
      </div>
    </div>
  );
}
