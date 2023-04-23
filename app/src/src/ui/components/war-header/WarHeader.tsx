import React, { CSSProperties, useCallback, useEffect, useState } from "react";
import styles from "./WarHeader.module.scss";
import dropdownVG from "../../../assets/dropdown.svg";
import { War, WarPhases } from "../../../models/War";
import { htmlService } from "../../../services/htmlService";

interface WarHeaderProps {
  children?: any;
  war: War;
}

export function WarHeader({ children, war }: WarHeaderProps) {
  const [ isExpended, setIsExpended ] = useState<boolean>(war.phase == WarPhases.preparation);
  const [ dropdownContentStyle, setDropdownContentStyle ] = useState<CSSProperties>({});

  useEffect(() => {
    if (isExpended) {
      expand();
    }
  }, []);

  const dropdownArrowClasses = [
    styles.dropdownArrow,
    isExpended ? styles.dropdownArrowRotated : "",
  ].join(" ");

  const toggleDropdown = useCallback(() => {
    const shouldExpand = !isExpended;
    setIsExpended(shouldExpand);
    shouldExpand ? expand() : collapse();
  }, [ isExpended ]);

  function expand(): void {
    const dropdownContentHeight = htmlService.getElementContentHeight("war-header-dropdown-content");
    setDropdownContentStyle({
      height: `${ dropdownContentHeight }px`,
      padding: "40px 0 70px",
    });
  }

  function collapse(): void {
    setDropdownContentStyle({
      height: 0,
      padding: 0,
    });
  }

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
