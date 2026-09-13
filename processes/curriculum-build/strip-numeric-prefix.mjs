// Section and track folders carry a numeric prefix purely to fix their
// display/build order (plain alphabetical sort put "classification"
// before "linear-regression", which is backwards pedagogically -- the
// same problem question folders already solved with their own "01-"
// prefixes). The prefix is not part of the semantic id: strip it before
// exposing `id`/`section`/`track`, so consumers keep working with
// "classical-ml"/"linear-regression", not "01-classical-ml".
export function stripNumericPrefix(dirName) {
	return dirName.replace(/^\d+-/, '');
}
