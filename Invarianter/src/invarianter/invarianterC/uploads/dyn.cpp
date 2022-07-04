#include <bits/stdc++.h>
using namespace std;

const int N = 3e5 + 5;

int n, m;
int d[N];
vector<int> kraw[N];
int dist[N];
int ile = 0;

int main()
{
	scanf("%d%d", &n, &m);
	for (int i = 1; i <= n; i++) {
		scanf("%d", &d[i]);
	}
	for (int i = 1; i < n; i++) {
		int a, b;
		scanf("%d%d", &a, &b);
		kraw[a].push_back(b);
		kraw[b].push_back(a);
	}
	
}
