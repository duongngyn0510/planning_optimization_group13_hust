#include <bits/stdc++.h>
using namespace std;
const int N = 1005, M = 105;
int n, m, t[N], g[N], s[N], c[M];
int l[N], bestl[N];
// l[i] : tiết bắt đầu của lớp i
// bestl[i] : lớp i được xếp vào tiết bestl[i]
//  (l[i] - 1)/6 == (l[i] + t[i] - 2)/6 (cùng 1 buổi học)
// g[i] = g[j] thì không được xếp trùng tiết

int r[N], bestr[N];
// r[i] : phòng học của lớp i
// bestr[i] : lớp i được xếp vào phòng bestr[i]
// s[i] <= c[r[i]] : lớp i có thể xếp vào phòng r[i]

int bestClass = 0, countClass = 0;
// bestClass: số lớp được xếp nhiều nhất
void input()
{
    cin >> n >> m;
    for (int i = 1; i <= n; i++)
    {
        cin >> t[i] >> g[i] >> s[i];
    }
    for (int i = 1; i <= m; i++)
    {
        cin >> c[i];
    }
    cout << "Input done" << endl;
}
void Solution()
{
    bestClass = countClass;
    for (int i = 1; i <= n; i++)
    {
        bestl[i] = l[i];
        bestr[i] = r[i];
    }
}
void Try(int i)
{
    bool checkValid = false;
    int k=1;
    while (k<=60-t[i]+1)
    {
        if ((k - 1) / 6 == (k + t[i] - 2) / 6)
        {
            for (int j = 1; j <= m; j++)
            {
                if (c[j] >= s[i])
                {
                    checkValid = true;
                    for (int p = 1; p <= i - 1; p++)
                    {
                        if ((l[p] <= k && k <= l[p] + t[p] - 1) || (k <= l[p] && l[p] <= k + t[i] - 1))
                        {
                            if (g[p] == g[i] || r[p] == j)
                            {
                                k = l[p] + t[p]-1;
                                checkValid = false;
                                break;
                            }
                        }
                    }
                    if (checkValid && (countClass + n - i + 1 > bestClass))
                    {
                        l[i] = k;
                        r[i] = j;
                        countClass++;
                        if (i == n)
                        {
                            if (countClass > bestClass)
                            {
                                Solution();
                            }
                        }
                        else
                        {
                            Try(i + 1);
                        }
                        countClass--;
                        l[i] = 0;
                        r[i] = 0;
                    }
                }
            }
        }
        else 
            k = ((k+t[i]-1)/6)*6;
        k++;
    }
    if (!checkValid && countClass + n - i + 1 > bestClass)
    {
        if (i == n)
        {
            if (countClass > bestClass)
            {
                Solution();
            }
        }
        else
        {
            Try(i + 1);
        }
    }
}

int main()
{
    input();
    Try(1);
    cout << bestClass << endl;
    for (int i = 1; i <= n; i++)
        if (bestl[i] != 0)
        {
            cout << i << " " << bestl[i] << " " << bestr[i] << endl;
        }
    return 0;
}

/*
10 2
4 1 15
4 1 18
4 1 15
2 2 18
4 2 11
3 1 15
2 2 27
3 2 18
4 1 13
3 1 10
20 20

7 2
4 1 15
4 1 18
4 1 15
2 2 18
4 2 11
2 2 27
3 2 18
20 20

6 2
4 1 15
4 1 18
4 1 15
2 2 18
2 2 27
3 2 18
20 20

5 2
4 1 15
4 1 18
4 1 15
2 2 27
3 2 18
20 20
*/