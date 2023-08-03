/**
 * Reduce cookie string to a Map.
 *
 * @returns {Map<string, string>}
 */
function getCookies() {
    // empty string, null or undefined returns empty Map
    if (!document.cookie) return new Map();

    return document.cookie.split(/\s*;\s*/g).reduce((map, current) => {
        const equalsIdx = current.indexOf("=");
        const key = current.substring(0, equalsIdx);
        const value = current.substring(equalsIdx + 1);

        map.set(key, value);
        return map;
    }, new Map());
}
