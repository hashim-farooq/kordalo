import { buildIslands } from "@framework/ui/vite/island";

await buildIslands({
	app: "kordalo",
	root: import.meta.dirname,
	entries: {
		"kordalo.project_costing": "src/project_costing/index.js",
		"kordalo.project_overview": "src/project_overview/index.js",
	},
	production: process.argv.includes("--production"),
	watch: process.argv.includes("--watch"),
});
