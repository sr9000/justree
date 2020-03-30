from justree import Tree


def main():
    t = Tree.from_tuple((1, [(5, []), (6, [('a', []), ('b', [])]), (7, [])]))
    g = Tree.from_tuple((1, [(5, []), (6, [('a', []), ('b', [])])]))

    print('1)', t)
    print('2)', g)
    print('3)', t == g)

    g.emplace(7)
    print('4)', g)
    print('5)', t == g)

    print('6)', g == g[()])
    print('7)', g[1])

    g[1, 0] = Tree(18)
    print('8)', g)

    del g[1, 1]
    print('9)', g)

    g.insert((1, 1), Tree('x'))
    print('10)', g)
    print('11)', len(g), g.size(), g.height())
    print('12)', g.value)

    print('13)', [x for x in g])
    print('14)', [Tree(value=5, children=()),
                  Tree(value=6, children=(Tree(value=18, children=()), Tree(value='x', children=()),)),
                  Tree(value=7, children=())])

    test = (1, [(2, [(5, [(14, []), (15, []), (16, [(23, []), (24, [])])]), (6, []), (7, [])]),
                (3, [(8, []), (9, [(17, []), (18, []), (19, [(25, []), (26, [])])]), (10, [])]),
                (4, [(11, []), (12, []), (13, [(20, []), (21, []), (22, [(27, []), (28, [])])])])])
    tg = Tree.from_tuple(test)
    print()
    print('15)', *[x.value for x in tg.bfs()])
    print('16)', *[x.value for x in tg.bfs(reverse=True)])
    print('17)', *[x.value for x in tg.bfs(mirror=True)])
    print('18)', *[x.value for x in tg.bfs(reverse=True, mirror=True)])
    print()
    print('19)', *[x.value for x in tg.dfs()])
    print('20)', *[x.value for x in tg.dfs(reverse=True)])
    print('21)', *[x.value for x in tg.dfs(mirror=True)])
    print('22)', *[x.value for x in tg.dfs(reverse=True, mirror=True)])
    print()
    print('23)', *[x.value for x in tg.dfs()])
    print('24)', *[x.value for x in tg.dfs(post_order=True, mirror=True)])
    print('25)', *[x.value for x in tg.dfs(mirror=True)])
    print('26)', *[x.value for x in tg.dfs(post_order=True)])
    print()

    ctg = tg.clone()
    print('27)', tg == ctg)

    del ctg[0]
    print('28)', tg == ctg, *[x.value for x in ctg.bfs()])

    ctg[()].value = []
    ctg.freeze()
    ctg2 = ctg.unfreeze()
    print('29)', ctg2 == ctg)

    del ctg2[0]
    print('30)', *[x.value for x in ctg.bfs()])
    print('31)', *[x.value for x in ctg2.bfs()])

    ctg2[()].value.append(13)
    print('32)', *[x.value for x in ctg.bfs()])
    print('33)', *[x.value for x in ctg2.bfs()])
    print('34)', ctg2.to_tuple())

    print('35)', *[(t.value, d, i) for t, d, i in ctg2.bfs_ex(depth=3)])
    print('36)', *[(t.value, d, i) for t, d, i in ctg2.dfs_ex(depth=3, post_order=True)])


if __name__ == '__main__':
    main()
