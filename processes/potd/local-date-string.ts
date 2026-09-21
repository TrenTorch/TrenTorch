// The visitor's own calendar date as 'YYYY-MM-DD'. Its own module because the
// IDE page needs it, and importing it from a module that also imports the
// curriculum would pull every question's text into that page's JavaScript.
export function localDateString(date: Date): string {
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, '0');
	const day = String(date.getDate()).padStart(2, '0');
	return `${year}-${month}-${day}`;
}
