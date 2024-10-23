import {defineConfig} from "vitepress";
import AutoSidebar from "vite-plugin-vitepress-auto-sidebar";

// https://vitepress.dev/zh/reference/site-config
// ref: https://gitee.com/zhontai/zhontai-admin-doc/blob/master/docs/.vitepress/config.ts
export default defineConfig({
    lang: "zh-CN",
    title: "Domain Admin-域名技术分享站",
    base: "/domain-admin/",
    ignoreDeadLinks: true,
    lastUpdated: true,
    markdown: {
        image: {
            // 默认禁用图片懒加载
            lazyLoading: true,
        },
    },
    head: [
        ["link", {rel: "icon", href: "https://demo.domain-admin.cn/favicon.ico"}],
        [
            'meta',
            {
                name: 'keywords',
                content: 'SSL,SSL证书监测,Let’s Encrypt,免费申请SSL证书,自动SSL证书续签,SSL证书到期提醒',
            },
        ],
        [
            'meta',
            {
                name: 'description',
                content: 'Domain Admin是域名和SSL证书监测平台，基于Let’s Encrypt实现免费申请SSL证书，自动SSL证书续签，SSL证书到期提醒，主要的竞品有：certd、okhttp、acme.sh、cetrbot',
            },
        ],
        // 百度统计
        [
            "script",
            {},
            `
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?1323b8c197b13150a6592146d5dbc928";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
`,
        ],
    ],
    sitemap: {
        hostname: "https://mouday.github.io/domain-admin",
    },
    locales: {
        "/": {
            lang: "zh-CN", // 设置为中文
        },
    },
    themeConfig: {
        search: {
            provider: "local",
            options: {
                translations: {
                    button: {
                        buttonText: "搜索文档",
                        buttonAriaLabel: "搜索文档",
                    },
                    modal: {
                        noResultsText: "无法找到相关结果",
                        resetButtonTitle: "清除查询条件",
                        displayDetails: "显示详细列表",
                        footer: {
                            navigateText: "切换",
                            selectText: "选择",
                            closeText: "关闭",
                        },
                    },
                },
            },
        },
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {text: "接口文档", link: "/api"},
            {text: "使用文档", link: "https://domain-admin.readthedocs.io/"},
        ],

        socialLinks: [
            {icon: "github", link: "https://github.com/dromara/domain-admin"},
            {icon: {
                svg: "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" t=\"1695538305440\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" p-id=\"1444\" style=\"width:1.25rem;height:1.25rem;vertical-align:middle;\"><path d=\"M512 1024C229.222 1024 0 794.778 0 512S229.222 0 512 0s512 229.222 512 512-229.222 512-512 512z m259.149-568.883h-290.74a25.293 25.293 0 0 0-25.292 25.293l-0.026 63.206c0 13.952 11.315 25.293 25.267 25.293h177.024c13.978 0 25.293 11.315 25.293 25.267v12.646a75.853 75.853 0 0 1-75.853 75.853h-240.23a25.293 25.293 0 0 1-25.267-25.293V417.203a75.853 75.853 0 0 1 75.827-75.853h353.946a25.293 25.293 0 0 0 25.267-25.292l0.077-63.207a25.293 25.293 0 0 0-25.268-25.293H417.152a189.62 189.62 0 0 0-189.62 189.645V771.15c0 13.977 11.316 25.293 25.294 25.293h372.94a170.65 170.65 0 0 0 170.65-170.65V480.384a25.293 25.293 0 0 0-25.293-25.267z\" fill=\"#C71D23\" p-id=\"1445\"></path></svg>",
                },
                link: "https://gitee.com/dromara/domain-admin"},
        ],

        outlineTitle: "导航目录",
        darkModeSwitchLabel: "外观",
        sidebarMenuLabel: "菜单",
        returnToTopLabel: "返回顶部",
        lastUpdatedText: "上次更新",
        outline: {
            /**
             * outline 中要显示的标题级别。
             * 单个数字表示只显示该级别的标题。
             * 如果传递的是一个元组，第一个数字是最小级别，第二个数字是最大级别。
             * `'deep'` 与 `[2, 6]` 相同，将显示从 `<h2>` 到 `<h6>` 的所有标题。
             *
             * @default 2
             */
            level: "deep",
            /**
             * 显示在 outline 上的标题。
             *
             * @default 'On this page'
             */
            label: "大纲",
        },

        sidebar: [],
        footer: {
            message: '<a href="https://beian.miit.gov.cn/" target="_blank">京ICP备2024081455号-2</a> | <a href="https://beian.mps.gov.cn/#/query/webSearch?code=11011302007323" rel="noreferrer" target="_blank">京公网安备11011302007323</a>',
            copyright: 'Copyright © 2024'
        }
    },
    vite: {
        plugins: [
            // https://github.com/QC2168/vite-plugin-vitepress-auto-sidebar
            AutoSidebar({
                ignoreList: ["/public/", "assets", "img", "demo"],
                titleFromFile: true,
                // 侧边栏排序
                beforeCreateSideBarItems: (data: string[]): string[] => {
                    // console.log(data);
                    // 通过正则提取文件名中的数字
                    function getOrder(item: string): number {
                        if (item == "index.md") {
                            return 0;
                        }
                        let res = item.match(/(?<order>\d+)/);
                        if (res && res.groups) {
                            return parseInt(res.groups.order);
                        } else {
                            return 999;
                        }
                    }

                    data.sort((a, b) => {
                        return getOrder(a) - getOrder(b);
                    });
                    return data.filter((n) => n != ".DS_Store");
                },
            }),
        ],
    },
    docFooter: {
        prev: "上一页",
        next: "下一页",
    },
});
