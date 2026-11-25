import {machineDesign} from './machine.js';
export const templates=Object.freeze([{id:'vacuum-demo',name:'Double chamber vacuum (concept test)',generate:machineDesign}]);
export function generateTemplate(id,params){const t=templates.find(t=>t.id===id);if(!t)throw Error('Unknown template');return t.generate(params)}
