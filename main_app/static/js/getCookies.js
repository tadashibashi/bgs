function getCookies() {
    if (!document.cookie) return new Map();

    return document.cookie.split(/\s*;\s*/g).reduce((accum, current) => {
        const equalsIdx = current.indexOf("=");
        const key = current.substring(0, equalsIdx);
        const value = current.substring(equalsIdx + 1);
        accum.set(key, value);
        return accum;
    }, new Map());
}
