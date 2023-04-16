import React, { CSSProperties, useCallback, useState } from "react";
import styles from "./WarHeader.module.scss";
import dropdownVG from "../../../assets/dropdown.svg";
import { War } from "../../../models/war";
import { htmlService } from "../../../services/htmlService";

interface WarHeaderProps {
  children?: any;
  war: War;
}

export function WarHeader({ children, war }: WarHeaderProps) {
  const [ isExpended, setIsExpended ] = useState<boolean>(false);
  const [ dropdownContentStyle, setDropdownContentStyle ] = useState<CSSProperties>({});

  const dropdownArrowClasses = [
    styles.dropdownArrow,
    isExpended ? styles.dropdownArrowRotated : "",
  ].join(" ");

  const toggleDropdown = useCallback(() => {
    const shouldExpand = !isExpended;
    setIsExpended(shouldExpand);
    const dropdownContentHeight = htmlService.getElementContentHeight("war-header-dropdown-content");
    setDropdownContentStyle({
      height: `${ shouldExpand ? dropdownContentHeight : 0 }px`,
      padding: shouldExpand ? "40px 0 70px" : "0",
    });
  }, [ isExpended ]);

  return (
    <div className={ styles.warHeader }>
      <div className={ styles.titleDropdownButton } onClick={ toggleDropdown }>
        <h1 className={ styles.title }>{ war.name }</h1>
        <img className={ dropdownArrowClasses } src={ dropdownVG } alt="carrot"/>
      </div>
      <div id="war-header-dropdown-content" className={ styles.titleDropdownContent } style={ dropdownContentStyle }>
        { children }
      </div>
    </div>
  );
}
