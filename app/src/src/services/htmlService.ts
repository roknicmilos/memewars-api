export const htmlService = {

  getElementContentHeight(elementID: string): number {
    let contentHeight = 0;
    const element: any = document.getElementById(elementID)!;
    for (const child of element.children) {
      contentHeight += child.clientHeight;
    }
    return contentHeight;
  },

};
