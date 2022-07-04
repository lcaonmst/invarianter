//https://szkopul.edu.pl/problemset/problem/bLHHUzy1-byoiJSbilgpI6Dc/site/?key=statement&fbclid=IwAR2-t6tCGR1e4qDY5SysxQcQp62iwcHQStNlU5_nuWeIyz2uULVl6CNMc7Y

#include <bits/stdc++.h>
using namespace std;

const int N = 1e6 + 5;

int n;
vector<int> kraw[N];
int rozm[N];
int odw[N];
int ile;
long long wyn[N];
int gleb[N];

void count_rozm(int x) {
	odw[x] = ile;
	rozm[x] = 1;
	for (int v : kraw[x]) {
		if (odw[v] != ile) {
			count_rozm(v);
			rozm[x] += rozm[v];
		}
	}
}

int longest(int x) {
	odw[x] = ile;
	int res = 0;
	for (int v : kraw[x]) {
		if (odw[v] != ile) {
			res = max(res, longest(v) + 1);
		}
	}
	return res;
}

void compute_gleb(int x) {
	odw[x] = ile;
	for (int v : kraw[x]) {
		if (odw[v] != ile) {
			gleb[v] = gleb[x] + 1;
			compute_gleb(v);
		}
	}
}

void find_centroid(int x, int ojc, int size) {
	bool centr = size <= n/2;
	int big = ojc;
	int wiel = size;
	for (int v : kraw[x]) {
		if (v != ojc && rozm[v] > n / 2) {
			centr = false;
		}
		if (v != ojc && rozm[v] > wiel) {
			big = v;
			wiel = rozm[v];
		}
	}
	if (!centr && big == ojc) {
		return;
	}
	if (!centr && big != ojc) {
		for (int v : kraw[x]) {
			if (v != ojc && v != big) {
				size += rozm[v];
			}
		}
		size++;
		find_centroid(big, x, size);
		return;
	}
	else {
		long long res = 0;
		ile++;
		if (wiel == n / 2 + n % 2) {
			odw[x] = ile;
			res = -longest(big) - 1;
		}
		else {
			res = -longest(x);
		}
		ile++;
		gleb[x] = 0;
		compute_gleb(x);
		for (int i = 1; i <= n; i++) {
			res += 2 * gleb[i];
		}
		wyn[x] = res;
	}
	if (big != ojc) {
		for (int v : kraw[x]) {
			if (v != ojc && v != big) {
				size += rozm[v];
			}
		}
		size++;
		find_centroid(big, x, size);
	}
}
	

int main()
{
	scanf("%d", &n);
	for (int i = 1; i < n; i++) {
		int a, b;
		scanf("%d%d", &a, &b);
		kraw[a].push_back(b);
		kraw[b].push_back(a);
	}
	for (int i = 1; i <= n; i++) {
		wyn[i] = -1;
	}
	ile++;
	count_rozm(1);
	find_centroid(1, 0, 0);
	for (int i = 1; i <= n; i++) {
		printf("%lld\n", wyn[i]);
	}
	
}
