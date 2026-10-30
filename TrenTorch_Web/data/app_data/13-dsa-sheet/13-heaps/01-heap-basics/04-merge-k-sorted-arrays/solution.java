import java.util.PriorityQueue;

public class Main {
    // O(N log k) time, O(k) space
    static long[] mergeKArrays(long[][] arrays) {
        if (arrays == null || arrays.length == 0) {
            return new long[0];
        }

        // Compute total length to allocate result array directly
        int totalLength = 0;
        for (long[] arr : arrays) {
            if (arr != null) {
                totalLength += arr.length;
            }
        }

        // Min-heap of (value, arrayIndex, elementIndex)
        PriorityQueue<HeapNode> heap = new PriorityQueue<>();
        for (int i = 0; i < arrays.length; i++) {
            if (arrays[i] != null && arrays[i].length > 0) {
                heap.offer(new HeapNode(arrays[i][0], i, 0));
            }
        }

        long[] result = new long[totalLength];
        int idx = 0;
        while (!heap.isEmpty()) {
            HeapNode node = heap.poll();
            result[idx++] = node.value;
            int nextIdx = node.elementIndex + 1;
            if (nextIdx < arrays[node.arrayIndex].length) {
                heap.offer(new HeapNode(arrays[node.arrayIndex][nextIdx], node.arrayIndex, nextIdx));
            }
        }
        return result;
    }

    // Helper record for heap elements (Java 17)
    private static record HeapNode(long value, int arrayIndex, int elementIndex) implements Comparable<HeapNode> {
        @Override
        public int compareTo(HeapNode other) {
            return Long.compare(this.value, other.value);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(mergeKArrays(new long[][]{new long[]{1L, 4L, 5L}, new long[]{1L, 3L, 4L}, new long[]{2L, 6L}})));
    }
}
