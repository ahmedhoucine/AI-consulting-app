import { MenuItem } from './menu.model';

export const MENU: MenuItem[] = [
    {
        id: 1,
        label: 'MENUITEMS.MENU.TEXT',
        isTitle: true
    },
    {
        id: 2,
        label: 'MENUITEMS.DASHBOARDS.TEXT',
        icon: 'bx-home-circle',
        link:'/dashboard'

    },
    {
        id: 3,
        label: 'MENUITEMS.RAPPORT.TEXT',
        icon: 'bx-chat',
        link: 'rapport',

    },
    {
        id: 4,
        label: 'MENUITEMS.RECOMMENDATION.TEXT',
        icon: 'bx-file',
        link: 'recommendation',
    },
    {
        id:5,
        label: 'MENUITEMS.ALERTES.TEXT',
        icon: 'bx-store',
        link:'alerte'
    },
    {
        id: 6,
        label: 'MENUITEMS.CONSEILS.TEXT',
        icon: 'bx-bitcoin',
        link:'matching',
    },
    {
        id: 7,
        label: 'MENUITEMS.FEEDBACKS.TEXT',
        icon: 'bx-envelope',
        link:'/tables/basic',
    },
    {
        id: 8,
        label: 'MENUITEMS.PREDICTIONS.TEXT',
        icon: 'bx-receipt',
        link:'/predict'
    },
    {
        id: 9,
        label: 'MENUITEMS.AUTHENTICATION.TEXT',
        icon: 'bx-briefcase-alt-2',
    },
]